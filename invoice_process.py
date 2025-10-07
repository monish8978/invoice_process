import json
import requests
import traceback
from io import BytesIO
from typing import Optional
import pytesseract
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from prompt_template import prompt_template
from logger import log
from settings import BITNET_URL, BITNET_MODEL_NAME, PORT

# ==============================
# FastAPI Setup
# ==============================
app = FastAPI(title="Invoice Parser API")

# ==============================
# Utilities
# ==============================

def ocr_image(image: Image.Image) -> str:
    """
    Perform OCR on the given image using pytesseract.
    Returns the extracted text as a string.
    """
    log.info("Starting OCR on image...")
    text = pytesseract.image_to_string(image)
    log.info(f"OCR completed. Extracted text length: {len(text)} characters.")
    return text

def clean_json_string(reply: str) -> str:
    """
    Clean response string by removing markdown-style code block wrappers.
    Example: ```json ... ```
    """
    reply = reply.strip()
    if reply.startswith("```json"):
        reply = reply[len("```json"):].strip()
    if reply.endswith("```"):
        reply = reply[:-3].strip()
    return reply

def get_invoice_data(invoice_text: str) -> dict:
    """
    Send the extracted invoice text to the model (BITNET) for parsing.
    Returns the parsed invoice data as a dictionary.
    """
    log.info("Preparing prompt for invoice parsing...")
    final_prompt = prompt_template.format(invoice_text=invoice_text)

    messages = [
        {"role": "system", "content": "You are an invoice extraction assistant."},
        {"role": "user", "content": final_prompt}
    ]

    payload = {
        "model": BITNET_MODEL_NAME,
        "messages": messages,
        "stream": False,
        "think": False
    }

    headers = {"Content-Type": "application/json"}

    try:
        log.info("Sending request to BITNET model...")
        response = requests.post(BITNET_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_data = response.json()

        # Extract reply content
        reply = None
        if "choices" in response_data:
            reply = response_data["choices"][0]["message"]["content"]
        elif "message" in response_data:
            reply = response_data["message"]["content"]

        if not reply:
            raise ValueError("No content found in model response.")

        log.info("Raw model reply received.")
        log.debug(f"Raw reply:\n{reply}")

        # Clean JSON string before parsing
        cleaned = clean_json_string(reply)

        try:
            parsed_json = json.loads(cleaned)
            log.info("Successfully parsed model response into JSON.")
            return parsed_json
        except json.JSONDecodeError:
            log.error("Failed to decode JSON from model response.")
            log.debug(f"Cleaned reply:\n{cleaned}")
            raise

    except Exception as e:
        log.error(f"Error in get_invoice_data: {str(e)}")
        traceback.print_exc()
        raise

# ==============================
# Unified API Endpoint
# ==============================
@app.post("/parse-invoice/")
async def parse_invoice(
    file: Optional[UploadFile] = File(None),
    image_url: Optional[str] = Form(None)
):
    """
    Unified endpoint for parsing invoices.
    Accepts either an uploaded image file or an image URL.
    """
    try:
        # Step 1: Load image
        if file:
            log.info(f"Received uploaded file: {file.filename}")
            image_bytes = await file.read()
            image = Image.open(BytesIO(image_bytes))
        elif image_url:
            log.info(f"Fetching image from URL: {image_url}")
            response = requests.get(image_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
        else:
            log.warning("No file or URL provided in request.")
            return JSONResponse(
                status_code=400,
                content={"error": "Provide either an image file or an image URL."}
            )

        # Step 2: Extract text using OCR
        invoice_text = ocr_image(image)
        if not invoice_text.strip():
            log.warning("OCR completed but no text detected in image.")
            return JSONResponse(status_code=400, content={"error": "No text detected in image."})

        # Step 3: Get parsed invoice data from the model
        parsed_data = get_invoice_data(invoice_text)
        log.info("Invoice parsed successfully.")
        return JSONResponse(content=parsed_data)

    except Exception as e:
        log.error(f"Exception in /parse-invoice/: {str(e)}")
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

# ==============================
# Run Locally (for development)
# ==============================
if __name__ == "__main__":
    import uvicorn
    log.info(f"Starting Invoice Parser API on port {PORT}...")
    uvicorn.run("invoice_process:app", host="0.0.0.0", port=PORT)

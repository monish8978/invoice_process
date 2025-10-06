# Invoice Parser API

A FastAPI-based service that extracts structured data from invoices using OCR and a language model (BITNET).  
The API can parse invoice images uploaded directly or via a URL and returns key invoice fields in JSON format.

---

## Features

- Extracts invoice text from images using **OCR (Tesseract via pytesseract)**.
- Sends extracted text to a language model (BITNET) to parse structured invoice fields.
- Returns invoice data as **JSON** with fields like:
  - `invoice_number`
  - `invoice_date`
  - `vendor_name`
  - `items` (list of `{description, quantity, price}`)
  - `subtotal`
  - `tax`
  - `total_amount`
- Supports both **file uploads** and **image URLs**.
- Detailed logging for debugging and monitoring.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/invoice_process.git
cd invoice_process
chmod +x create_env.sh
./create_env.sh

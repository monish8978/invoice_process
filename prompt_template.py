from langchain.prompts import PromptTemplate

# ==============================
# Prompt Template for Invoice Parsing
# ==============================
# This template defines how the extracted invoice text should be
# processed by a language model to produce structured JSON data.
# Using LangChain's PromptTemplate allows us to dynamically insert
# invoice text into the prompt before sending it to the model.

prompt_template = PromptTemplate(
    # Variables that can be dynamically replaced in the template
    input_variables=["invoice_text"],

    # The template string that instructs the model
    template="""
You are an intelligent invoice parser.

# Instruction to the model
# Ask the model to extract key fields from the invoice text
# and format them as valid JSON.
Extract key fields from the following invoice text and return only valid JSON.

# Placeholder for actual invoice text (injected dynamically)
Invoice Text:
{invoice_text}

# Specify which fields to extract and their expected structure
Extracted JSON fields:
- invoice_number       # e.g., "INV-12345"
- invoice_date         # e.g., "2025-10-06"
- vendor_name          # Name of the vendor/supplier
- items (list of {{description, quantity, price}})  # List of items in invoice
- subtotal             # Sum of item totals before tax
- tax                  # Tax amount
- total_amount         # Final invoice total

# Emphasize that the model should return only valid JSON without any explanation
Return only valid JSON without explanation.
"""
)

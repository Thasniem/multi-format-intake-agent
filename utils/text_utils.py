#utils/text_utils.py
import re

def is_text_document(content):
    """
    Heuristically determine if a string is a plain text document.
    """
    if not isinstance(content, str):
        return False

    content_lower = content.lower()
    invoice_keywords = ["invoice number", "total amount", "customer", "date"]
    return any(keyword in content_lower for keyword in invoice_keywords)

def extract_text_fields(text):
    """
    Extract common fields from plain text documents like invoices using simple keyword rules.
    """
    fields = {}

    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if line.lower().startswith("invoice number"):
            fields["invoice_number"] = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("date"):
            fields["date"] = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("customer"):
            fields["customer"] = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("total amount"):
            fields["total_amount"] = line.split(":", 1)[-1].strip()

    return fields

def detect_text_intent(text):
    """
    Detect intent from plain text using keyword heuristics.
    """
    text = text.lower()
    if "invoice" in text:
        return "invoice"
    elif "rfq" in text or "quotation" in text:
        return "rfq"
    elif "complaint" in text or "issue" in text:
        return "complaint"
    elif "regulation" in text or "policy" in text:
        return "regulation"
    return "general"

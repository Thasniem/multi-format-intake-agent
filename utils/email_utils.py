# utils/email_utils.py
import re

def is_email(text):
    """
    Heuristically determine if a string is an email message.
    """
    return "@" in text and ("From:" in text or "Subject:" in text)

def parse_email_body(email_text):
    """
    Very basic email parser - in real scenarios, use `email` or `mailparser` libraries.
    """
    sender_match = re.search(r"From:\s*(.*)", email_text)
    subject_match = re.search(r"Subject:\s*(.*)", email_text)
    urgency_match = re.search(r"\burgent\b|\basap\b|\bimmediately\b", email_text, re.IGNORECASE)

    return {
        "sender": sender_match.group(1).strip() if sender_match else "unknown",
        "intent": extract_intent_from_text(email_text),
        "urgency": bool(urgency_match),
        "conversation_id": extract_conversation_id(email_text),
    }

def extract_conversation_id(text):
    """
    Dummy function to simulate thread ID extraction.
    """
    match = re.search(r"Conversation-ID:\s*(\S+)", text)
    return match.group(1) if match else None

def extract_intent_from_text(text):
    """
    Simple keyword-based intent detection.
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

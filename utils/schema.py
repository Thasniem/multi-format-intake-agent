# utils/schema.py

class FlowBitSchema:
    """
    Defines required fields and validates incoming JSON payloads
    for FlowBit format.
    """
    def __init__(self):
        self.required_fields = [
            "request_id", "timestamp", "customer_name",
            "request_type", "items", "priority"
        ]

    def validate_and_extract(self, data):
        extracted = {}
        anomalies = []

        for field in self.required_fields:
            if field in data:
                extracted[field] = data[field]
            else:
                anomalies.append(f"Missing required field: {field}")

        return extracted, anomalies


def detect_intent(content):
    """
    Shared utility for intent detection, used by ClassifierAgent.
    """
    if isinstance(content, str):
        text = content.lower()
    elif isinstance(content, bytes):
        text = content.decode(errors='ignore').lower()
    else:
        text = str(content).lower()

    if "invoice" in text:
        return "invoice"
    elif "rfq" in text:
        return "rfq"
    elif "complaint" in text:
        return "complaint"
    elif "regulation" in text:
        return "regulation"
    return "general"

from utils.text_utils import extract_text_fields
from memory.memory import Memory

class TextAgent:
    def __init__(self, memory: Memory):
        self.memory = memory

    def handle_text(self, text: str) -> dict:
        """
        Process plain text input and extract structured fields.

        Args:
            text (str): Plain text input (e.g., invoice content).

        Returns:
            dict: Extracted fields like invoice_number, date, customer, total_amount.
        """
        extracted = extract_text_fields(text)
        self.memory.store_fields("text_agent", extracted)
        return extracted

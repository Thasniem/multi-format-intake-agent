# agents/email_agent.py

from utils.email_utils import parse_email_body

class EmailAgent:
    def __init__(self, memory):
        self.memory = memory

    def handle_email(self, email_text: str) -> dict:
        """
        Process raw email text, extract structured information,
        and store extracted fields in memory.

        Args:
            email_text (str): Raw email content as string.

        Returns:
            dict: Extracted fields including sender, intent, urgency, and optional conversation_id.
        """
        parsed = parse_email_body(email_text)

        record = {
            'sender': parsed.get('sender'),
            'intent': parsed.get('intent'),
            'urgency': parsed.get('urgency'),
            'conversation_id': parsed.get('conversation_id')
        }

        self.memory.store_fields('email_agent', record)
        return record

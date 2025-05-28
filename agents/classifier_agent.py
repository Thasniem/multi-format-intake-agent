# agents/classifier_agent.py

import json
from typing import Tuple

class ClassifierAgent:
    def __init__(self, memory):
        self.memory = memory

    def classify(self, raw_input: str, metadata: dict) -> Tuple[str, str]:
        """
        Classify the input data format and intent.

        Returns:
            tuple: (format, intent)
            format: one of ["json", "email", "pdf", "text", "unknown"]
            intent: one of ["invoice", "rfq", "complaint", "regulation", "unknown"]
        """
        raw_input_lower = raw_input.lower()

        # Try parsing as JSON
        try:
            parsed = json.loads(raw_input)
            intent = self._detect_intent_json(parsed)
            self.memory.store_metadata({"format": "json", "intent": intent, **metadata})
            return "json", intent
        except Exception:
            pass

        # Check if input looks like an email (basic heuristic)
        if raw_input_lower.startswith("from:") or "subject:" in raw_input_lower:
            intent = self._detect_intent_email(raw_input)
            self.memory.store_metadata({"format": "email", "intent": intent, **metadata})
            return "email", intent

        # Check if input looks like a PDF (placeholder)
        if raw_input_lower.startswith("%pdf") or raw_input_lower.startswith("pdf"):
            intent = self._detect_intent_pdf(raw_input)
            self.memory.store_metadata({"format": "pdf", "intent": intent, **metadata})
            return "pdf", intent

        # Check if input is plain text with invoice-like keywords
        invoice_keywords = ["invoice number", "total amount", "customer", "date"]
        if any(keyword in raw_input_lower for keyword in invoice_keywords):
            intent = "invoice"
            self.memory.store_metadata({"format": "text", "intent": intent, **metadata})
            return "text", intent

        # Fallback unknown format and intent
        self.memory.store_metadata({"format": "unknown", "intent": "unknown", **metadata})
        return "unknown", "unknown"

    def _detect_intent_json(self, data: dict) -> str:
        """
        Detect intent based on JSON keys/content.
        """
        if "invoice_id" in data or "invoice_number" in data:
            return "invoice"
        if "rfq" in json.dumps(data).lower():
            return "rfq"
        return "unknown"

    def _detect_intent_email(self, text: str) -> str:
        """
        Detect intent from email text content.
        """
        text_lower = text.lower()
        if "invoice" in text_lower:
            return "invoice"
        if "rfq" in text_lower or "request for quote" in text_lower:
            return "rfq"
        if "complaint" in text_lower:
            return "complaint"
        return "unknown"

    def _detect_intent_pdf(self, text: str) -> str:
        """
        Placeholder for PDF intent detection.
        """
        return "unknown"

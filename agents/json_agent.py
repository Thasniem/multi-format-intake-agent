# agents/json_agent.py

import json
from typing import Union, Dict, Any
from utils.schema import FlowBitSchema

class JSONAgent:
    def __init__(self, memory):
        self.memory = memory

    def handle_json(self, json_input: str) -> Dict[str, Union[Dict[str, Any], str]]:
        """
        Parse JSON input, validate and extract fields using schema,
        store the extracted data in memory, and return extracted data and anomalies.

        Args:
            json_input (str): JSON string input.

        Returns:
            dict: {
                'extracted': dict of validated and extracted fields,
                'anomalies': list of anomalies found,
                OR
                'error': error message if JSON is invalid
            }
        """
        try:
            data = json.loads(json_input)
        except json.JSONDecodeError:
            return {'error': 'Invalid JSON'}

        schema = FlowBitSchema()
        extracted, anomalies = schema.validate_and_extract(data)

        self.memory.store_fields('json_agent', extracted)

        return {
            'extracted': extracted,
            'anomalies': anomalies
        }

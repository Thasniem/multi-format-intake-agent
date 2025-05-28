import datetime

class Memory:
    def __init__(self):
        self.data = {
            'metadata': [],
            'fields': {}
        }

    def store_metadata(self, metadata):
        metadata['timestamp'] = metadata.get('timestamp') or datetime.datetime.utcnow().isoformat()
        self.data['metadata'].append(metadata)
        print(f"[Memory] Stored metadata: {metadata}")

    def store_fields(self, agent_name, fields):  # renamed here
        if agent_name not in self.data['fields']:
            self.data['fields'][agent_name] = []
        self.data['fields'][agent_name].append(fields)
        print(f"[Memory] Stored fields for {agent_name}: {fields}")

    def get_all_metadata(self):
        return self.data['metadata']

    def get_agent_fields(self, agent_name):
        return self.data['fields'].get(agent_name, [])

    def clear(self):
        self.data = {
            'metadata': [],
            'fields': {}
        }

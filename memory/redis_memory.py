# memory/redis_memory.py

import json
import datetime
import redis

class RedisMemory:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def store_metadata(self, metadata):
        metadata['timestamp'] = metadata.get('timestamp') or datetime.datetime.utcnow().isoformat()
        self.redis_client.rpush('metadata', json.dumps(metadata))
        print(f"[RedisMemory] Stored metadata: {metadata}")

    def store_agent_fields(self, agent_name, fields):
        key = f"fields:{agent_name}"
        self.redis_client.rpush(key, json.dumps(fields))
        print(f"[RedisMemory] Stored fields for {agent_name}: {fields}")

    def get_all_metadata(self):
        return [json.loads(item) for item in self.redis_client.lrange('metadata', 0, -1)]

    def get_agent_fields(self, agent_name):
        key = f"fields:{agent_name}"
        return [json.loads(item) for item in self.redis_client.lrange(key, 0, -1)]

    def clear(self):
        self.redis_client.flushdb()
        print("[RedisMemory] Cleared all memory")

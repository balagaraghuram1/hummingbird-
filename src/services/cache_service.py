import json

import redis

from src.config.settings import settings


class CacheService:
    def __init__(self) -> None:
        self.client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

    def get_json(self, key: str) -> dict | None:
        raw = self.client.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    def set_json(self, key: str, value: dict, ttl_seconds: int = 300) -> None:
        self.client.setex(key, ttl_seconds, json.dumps(value))


cache_service = CacheService()


"""Redis cache service.

Provides JSON-based caching with automatic serialization
and configurable TTL for API responses and AI results.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from src.config.settings import settings

logger = logging.getLogger(__name__)


class CacheService:
    """Redis-backed cache service for medical AI data.

    Provides get/set operations with automatic JSON serialization
    and configurable TTL. Handles Redis connection failures gracefully.
    """

    def __init__(self) -> None:
        self._client = None
        self._available = False

    def _ensure_client(self) -> None:
        """Lazy-initialize the Redis client."""
        if self._client is not None:
            return

        try:
            import redis
            self._client = redis.Redis.from_url(
                settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
            )
            self._client.ping()
            self._available = True
            logger.info("Redis cache connected successfully")
        except Exception as e:
            logger.warning("Redis unavailable, caching disabled: %s", e)
            self._available = False

    def get_json(self, key: str) -> dict[str, Any] | None:
        """Retrieve a JSON value from cache.

        Args:
            key: Cache key.

        Returns:
            Parsed JSON dict or None if not found/unavailable.
        """
        self._ensure_client()
        if not self._available:
            return None

        try:
            raw = self._client.get(key)
            if raw is None:
                return None
            return json.loads(raw)
        except Exception as e:
            logger.warning("Cache get failed for key %s: %s", key, e)
            return None

    def set_json(self, key: str, value: dict[str, Any], ttl_seconds: int = 300) -> bool:
        """Store a JSON value in cache.

        Args:
            key: Cache key.
            value: Dictionary to cache.
            ttl_seconds: Time-to-live in seconds.

        Returns:
            True if stored successfully, False otherwise.
        """
        self._ensure_client()
        if not self._available:
            return False

        try:
            self._client.setex(key, ttl_seconds, json.dumps(value, default=str))
            return True
        except Exception as e:
            logger.warning("Cache set failed for key %s: %s", key, e)
            return False

    def delete(self, key: str) -> bool:
        """Delete a key from cache.

        Args:
            key: Cache key to delete.

        Returns:
            True if deleted, False otherwise.
        """
        self._ensure_client()
        if not self._available:
            return False

        try:
            self._client.delete(key)
            return True
        except Exception as e:
            logger.warning("Cache delete failed for key %s: %s", key, e)
            return False

    def flush_pattern(self, pattern: str) -> int:
        """Delete all keys matching a pattern.

        Args:
            pattern: Redis key pattern (e.g., "diagnose:*").

        Returns:
            Number of keys deleted.
        """
        self._ensure_client()
        if not self._available:
            return 0

        try:
            keys = list(self._client.scan_iter(match=pattern, count=1000))
            if keys:
                return self._client.delete(*keys)
            return 0
        except Exception as e:
            logger.warning("Cache flush failed for pattern %s: %s", pattern, e)
            return 0

    @property
    def is_available(self) -> bool:
        """Check if Redis is connected and available."""
        self._ensure_client()
        return self._available


cache_service = CacheService()
# v8 - updated 2026-06-11

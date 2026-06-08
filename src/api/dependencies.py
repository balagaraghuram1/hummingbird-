"""API dependencies for dependency injection.

Provides reusable dependencies for authentication,
rate limiting, and request validation.
"""

from __future__ import annotations

import logging
import time
from collections import defaultdict
from typing import Any

from fastapi import Header, HTTPException, Request

from src.config.settings import settings

logger = logging.getLogger(__name__)

_rate_limit_store: dict[str, list[float]] = defaultdict(list)


async def require_api_key(
    x_api_key: str | None = Header(default=None),
) -> str:
    """Validate API key from request header.

    Args:
        x_api_key: API key from X-API-Key header.

    Returns:
        The validated API key.

    Raises:
        HTTPException: If API key is missing or invalid.
    """
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API key. Include X-API-Key header.",
        )

    if len(x_api_key) < 16:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key format.",
        )

    return x_api_key


async def check_rate_limit(request: Request) -> None:
    """Check rate limit for the current request.

    Uses a simple sliding window counter per client IP.

    Args:
        request: FastAPI request object.

    Raises:
        HTTPException: If rate limit is exceeded.
    """
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    window = 60.0

    _rate_limit_store[client_ip] = [
        t for t in _rate_limit_store[client_ip] if now - t < window
    ]

    if len(_rate_limit_store[client_ip]) >= settings.rate_limit_per_minute:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later.",
        )

    _rate_limit_store[client_ip].append(now)


async def get_current_user(
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """Extract and validate the current user from JWT token.

    Args:
        authorization: Bearer token from Authorization header.

    Returns:
        User information dictionary.

    Raises:
        HTTPException: If token is missing or invalid.
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization header. Use Bearer token.",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization format. Use: Bearer <token>",
        )

    token = authorization[7:]

    try:
        from src.config.security import verify_token
        payload = verify_token(token)
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid or expired token: {e}",
        ) from e
# v6 - updated 2026-06-11
# v36 - updated 2026-06-11
# v66 - updated 2026-06-11
# v96 - updated 2026-06-11

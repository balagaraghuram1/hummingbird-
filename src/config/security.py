"""Security utilities for authentication and password hashing.

Provides JWT token creation/verification and bcrypt password hashing.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.config.settings import settings

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a bcrypt hash.

    Args:
        plain_password: The plain text password.
        hashed_password: The bcrypt hash to verify against.

    Returns:
        True if the password matches.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a bcrypt hash of a password.

    Args:
        password: The plain text password to hash.

    Returns:
        The bcrypt hash string.
    """
    return pwd_context.hash(password)


def create_access_token(
    subject: str,
    expires_minutes: int | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """Create a JWT access token.

    Args:
        subject: The token subject (usually user ID).
        expires_minutes: Token expiration in minutes.
        extra_claims: Additional claims to include.

    Returns:
        Encoded JWT token string.
    """
    expire_delta = timedelta(
        minutes=expires_minutes or settings.access_token_expire_minutes
    )
    payload: dict[str, Any] = {
        "sub": subject,
        "iat": datetime.now(tz=timezone.utc),
        "exp": datetime.now(tz=timezone.utc) + expire_delta,
    }
    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def verify_token(token: str) -> dict[str, Any]:
    """Verify and decode a JWT token.

    Args:
        token: The JWT token string to verify.

    Returns:
        Decoded token payload.

    Raises:
        JWTError: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        return payload
    except JWTError as e:
        logger.warning("Token verification failed: %s", e)
        raise
# v3 - updated 2026-06-11
# v33 - updated 2026-06-11

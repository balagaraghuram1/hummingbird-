"""Utility helpers for common operations.

Provides date/time utilities, string manipulation,
and other shared helper functions.
"""

from __future__ import annotations

import hashlib
import re
import uuid
from datetime import datetime, timezone


def utc_now_iso() -> str:
    """Get current UTC time as ISO 8601 string.

    Returns:
        ISO 8601 formatted datetime string.
    """
    return datetime.now(timezone.utc).isoformat()


def generate_request_id() -> str:
    """Generate a unique request ID.

    Returns:
        8-character UUID string.
    """
    return str(uuid.uuid4())[:8]


def sanitize_input(text: str, max_length: int = 5000) -> str:
    """Sanitize user input text.

    Removes potentially dangerous characters and limits length.

    Args:
        text: Input text to sanitize.
        max_length: Maximum allowed length.

    Returns:
        Sanitized text string.
    """
    text = text.strip()
    text = re.sub(r"[<>&\"']", "", text)
    text = text[:max_length]
    return text


def hash_text(text: str) -> str:
    """Generate SHA-256 hash of text.

    Args:
        text: Text to hash.

    Returns:
        Hex digest of SHA-256 hash.
    """
    return hashlib.sha256(text.encode()).hexdigest()


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to a maximum length with suffix.

    Args:
        text: Text to truncate.
        max_length: Maximum length including suffix.
        suffix: Suffix to append if truncated.

    Returns:
        Truncated text string.
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix
# v18 - updated 2026-06-11
# v48 - updated 2026-06-11
# v78 - updated 2026-06-11

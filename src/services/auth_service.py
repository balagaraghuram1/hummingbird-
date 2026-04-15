"""Authentication service.

Handles user authentication, password hashing, and token management.
"""

from __future__ import annotations

import logging

from src.config.security import create_access_token, get_password_hash, verify_password

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication service for user management.

    Provides password hashing, verification, and JWT token issuance.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt.

        Args:
            password: Plain text password.

        Returns:
            Bcrypt hash string.
        """
        return get_password_hash(password)

    @staticmethod
    def check_password(password: str, hashed: str) -> bool:
        """Verify a password against a hash.

        Args:
            password: Plain text password.
            hashed: Bcrypt hash to verify against.

        Returns:
            True if password matches.
        """
        return verify_password(password, hashed)

    @staticmethod
    def issue_token(user_id: str, expires_minutes: int | None = None) -> str:
        """Issue a JWT access token for a user.

        Args:
            user_id: The user's unique identifier.
            expires_minutes: Token expiration time.

        Returns:
            JWT access token string.
        """
        return create_access_token(subject=user_id, expires_minutes=expires_minutes)

    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """Validate password strength.

        Args:
            password: Password to validate.

        Returns:
            Tuple of (is_valid, error_message).
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        return True, ""


auth_service = AuthService()
# v10 - updated 2026-06-11
# v40 - updated 2026-06-11
# v70 - updated 2026-06-11

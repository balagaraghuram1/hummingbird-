"""Application exception classes.

Defines custom exceptions for structured error handling
across the application.
"""

from __future__ import annotations


class HummingbirdError(Exception):
    """Base exception for the Hummingbird application."""

    def __init__(self, message: str = "An error occurred") -> None:
        self.message = message
        super().__init__(self.message)


class AIProviderError(HummingbirdError):
    """Raised when an AI provider call fails."""

    def __init__(self, message: str = "AI provider error") -> None:
        super().__init__(message)
        self.error_code = "AI_PROVIDER_ERROR"


class ValidationError(HummingbirdError):
    """Raised when input validation fails."""

    def __init__(self, message: str = "Validation error") -> None:
        super().__init__(message)
        self.error_code = "VALIDATION_ERROR"


class ServiceUnavailableError(HummingbirdError):
    """Raised when a required service is unavailable."""

    def __init__(self, service: str = "unknown") -> None:
        message = f"Service unavailable: {service}"
        super().__init__(message)
        self.error_code = "SERVICE_UNAVAILABLE"
        self.service = service


class AuthenticationError(HummingbirdError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message)
        self.error_code = "AUTHENTICATION_ERROR"


class RateLimitError(HummingbirdError):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__(message)
        self.error_code = "RATE_LIMIT_ERROR"
# v20 - updated 2026-06-11

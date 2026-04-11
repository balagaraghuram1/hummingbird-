class HummingbirdError(Exception):
    """Base application exception."""


class AIProviderError(HummingbirdError):
    """Raised when an AI provider call fails."""


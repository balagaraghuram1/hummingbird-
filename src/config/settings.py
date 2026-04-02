"""Application configuration settings.

Loads configuration from environment variables and .env files.
Uses pydantic-settings for type-safe configuration management.
"""

from __future__ import annotations

import secrets
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")

    # Application
    app_name: str = Field(default="Hummingbird Medical AI", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")

    # AI Provider
    openai_api_key: str | None = Field(default=None, description="OpenAI API key")
    anthropic_api_key: str | None = Field(default=None, description="Anthropic API key")
    model_name: str = Field(default="gpt-4o", description="Primary LLM model name")
    model_temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    model_max_tokens: int = Field(default=1500, ge=1, le=128000)

    # Database
    database_url: str = Field(default="sqlite:///./hummingbird.db", description="Database URL")
    redis_url: str = Field(default="redis://localhost:6379", description="Redis connection URL")
    chroma_persist_directory: str = Field(default="./data/chroma_db")

    # Security
    secret_key: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30, ge=1)
    refresh_token_expire_days: int = Field(default=7, ge=1)

    # CORS
    cors_origins: list[str] = Field(default=["http://localhost:3000", "http://localhost:8000"])

    # Rate limiting
    rate_limit_per_minute: int = Field(default=60, ge=1)
    rate_limit_per_hour: int = Field(default=1000, ge=1)

    # Medical AI
    max_diagnosis_results: int = Field(default=5, ge=1)
    treatment_confidence_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    enable_medical_validation: bool = Field(default=True)

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v:
            raise ValueError("DATABASE_URL cannot be empty")
        return v

    @property
    def is_ai_configured(self) -> bool:
        """Check if at least one AI provider is configured."""
        return bool(self.openai_api_key or self.anthropic_api_key)

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.debug


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
# v1 - updated 2026-06-11
# v31 - updated 2026-06-11
# v61 - updated 2026-06-11

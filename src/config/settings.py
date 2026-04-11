from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = Field(default="Hummingbird Medical AI")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")

    openai_api_key: str | None = Field(default=None)
    anthropic_api_key: str | None = Field(default=None)
    model_name: str = Field(default="gpt-4o")
    model_temperature: float = Field(default=0.2)
    model_max_tokens: int = Field(default=1500)

    database_url: str = Field(default="sqlite:///./hummingbird.db")
    redis_url: str = Field(default="redis://localhost:6379")
    chroma_persist_directory: str = Field(default="./data/chroma_db")

    secret_key: str = Field(default="change_me")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)


settings = Settings()


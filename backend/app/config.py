from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Professional POS System"
    app_env: str = "development"
    debug: bool = True
    api_prefix: str = "/api"

    host: str = "0.0.0.0"
    port: int = 8000

    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/pos_system"
    )

    secret_key: str = "CHANGE_THIS_SECRET_KEY"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    default_currency: str = "PKR"
    default_timezone: str = "Asia/Karachi"

    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    default_admin_username: str = "admin"
    default_admin_password: str = "CHANGE_THIS_PASSWORD"

    upload_dir: str = "uploads"
    max_upload_size_mb: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if isinstance(value, str):
            return [
                origin.strip()
                for origin in value.split(",")
                if origin.strip()
            ]

        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

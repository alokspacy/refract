import os
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "AccessLearn AI"
    VERSION: str = "0.1.0"
    API_V1_STR: str = ""
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = "postgresql://accesslearn:accesslearn_secure_pass@localhost:5432/accesslearn_db"

    # Redis & Queue
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Security & JWT
    JWT_SECRET: str = "super_secret_jwt_signing_key_change_in_production_min_32_chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Storage
    STORAGE_PROVIDER: str = "local"
    LOCAL_STORAGE_PATH: str = "./storage"
    MAX_FILE_SIZE_MB: int = 50

    # Allowed extensions
    ALLOWED_EXTENSIONS: Union[List[str], str] = [
        "pdf", "docx", "pptx", "png", "jpg", "jpeg", "txt", "mp3", "wav", "mp4"
    ]

    # CORS
    ALLOWED_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
        "http://localhost:3003",
        "http://127.0.0.1:3003",
        "http://localhost:8000"
    ]

    @field_validator("ALLOWED_EXTENSIONS", mode="after")
    @classmethod
    def parse_allowed_extensions(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [ext.strip().lower().lstrip(".") for ext in v.split(",") if ext.strip()]
        return [ext.strip().lower().lstrip(".") for ext in v]

    @field_validator("ALLOWED_ORIGINS", mode="after")
    @classmethod
    def parse_allowed_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

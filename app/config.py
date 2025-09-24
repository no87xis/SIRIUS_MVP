import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./sirius.db"
    database_pool_size: int = 5
    database_max_overflow: int = 10
    database_pool_timeout: int = 30
    database_pool_recycle: int = 3600
    
    # Security
    secret_key: str = "mvp-secret-key-32-characters-long-2024"
    session_max_age: int = 86400  # 24 hours
    
    # Timeouts (в секундах)
    http_timeout: int = 10
    database_timeout: int = 5
    startup_timeout: int = 30
    
    # Environment
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"
    
    # MVP: Уведомления полностью отключены
    # Все переменные уведомлений игнорируются
    
    @field_validator('secret_key')
    @classmethod
    def validate_secret_key(cls, v):
        if v == "dev-secret-key-change-in-production" and os.getenv("ENVIRONMENT") == "production":
            raise ValueError("SECRET_KEY must be changed in production")
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v

    model_config = {
        "case_sensitive": False,
        "env_file": [".env", "env.mvp"],  # Поддержка MVP конфигурации
        "env_file_encoding": "utf-8"
    }


# Используем только переменные окружения и значения по умолчанию
settings = Settings()

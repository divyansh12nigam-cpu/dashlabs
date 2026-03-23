import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    # WhatsApp Cloud API
    WHATSAPP_TOKEN: str = ""
    WHATSAPP_PHONE_NUMBER_ID: str = ""
    VERIFY_TOKEN: str = "dashlabs_verify_2024"

    # Admin notifications
    ADMIN_PHONE: str = "919625922022"
    ADMIN_EMAIL: str = "hello@dashlabs.in"

    # Email (SMTP)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/dashlabs.db"

    # App
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    # Conversation timeout in minutes
    CONVERSATION_TIMEOUT_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()

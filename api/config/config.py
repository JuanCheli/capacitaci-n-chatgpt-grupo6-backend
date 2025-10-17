from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Gemini (or other LLM) credentials
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # App settings
    APP_NAME: str = "Simulador ChatGPT - Capacitación"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

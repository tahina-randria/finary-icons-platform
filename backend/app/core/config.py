"""
Configuration settings for Finary Icons Platform
Uses Pydantic Settings to load from environment variables
"""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Project Info
    PROJECT_NAME: str = "Finary Icons Platform"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API Keys
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    REPLICATE_API_TOKEN: str = ""
    YOUTUBE_API_KEY: str = ""

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""

    # Redis (for Celery)
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://finary-icons.vercel.app"
    ]

    # Image Generation Settings
    DEFAULT_IMAGE_SIZE: str = "2048x2048"
    SUPPORTED_IMAGE_SIZES: List[str] = ["1024x1024", "2048x2048", "4096x4096"]

    # Storage
    ICONS_STORAGE_BUCKET: str = "icons"
    MAX_UPLOAD_SIZE_MB: int = 10

    # Generation Settings
    MAX_CONCEPTS_PER_VIDEO: int = 50
    DEFAULT_ICON_STYLE: str = "finary-glass-3d"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    Uses lru_cache to ensure singleton pattern
    """
    return Settings()


# Export singleton instance
settings = get_settings()

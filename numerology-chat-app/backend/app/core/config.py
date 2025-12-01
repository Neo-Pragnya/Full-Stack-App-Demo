"""
Configuration settings for the Numerology Chat API.
"""

import os
from typing import List


class Settings:
    """Application settings."""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Numerology Chat API"
    VERSION: str = "1.0.0"
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:4200",  # Angular dev server
        "http://localhost:3000",  # Alternative frontend port
        "http://127.0.0.1",
        "http://127.0.0.1:4200",
    ]
    
    # Security Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    # Database Settings (for future use)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./numerology.db")
    
    # Logging Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Session Settings
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))
    
    # Rate Limiting (for future use)
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100"))


# Create settings instance
settings = Settings()
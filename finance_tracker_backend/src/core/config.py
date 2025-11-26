from functools import lru_cache
import os
from typing import Optional

from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


class Settings(BaseModel):
    """Application settings loaded from environment variables."""

    DATABASE_URL: str = Field(default=os.getenv("DATABASE_URL", "sqlite:///./data.db"))
    JWT_SECRET: str = Field(default=os.getenv("JWT_SECRET", "change-me"))
    JWT_ALG: str = Field(default=os.getenv("JWT_ALG", "HS256"))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    )
    # CORS settings placeholders (can be extended later)
    CORS_ALLOW_ORIGINS: Optional[str] = Field(default=os.getenv("CORS_ALLOW_ORIGINS", "*"))


# PUBLIC_INTERFACE
@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()

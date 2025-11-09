"""
Configuration Settings
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "Aero Elite"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # API
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]

    # Database
    DATABASE_URL: str = "postgresql://aeroelite:aeroelite_password@localhost:5432/aeroelite"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Google Cloud Platform
    GCP_PROJECT_ID: str = ""
    VERTEX_AI_LOCATION: str = "us-central1"
    GEMINI_API_KEY: str = ""
    CLOUD_STORAGE_BUCKET: str = "aeroelite-models"

    # Authentication
    JWT_SECRET: str = "your-super-secret-jwt-key-change-this"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Google OAuth
    GOOGLE_OAUTH_CLIENT_ID: str = ""
    GOOGLE_OAUTH_CLIENT_SECRET: str = ""
    GOOGLE_OAUTH_REDIRECT_URI: str = "http://localhost:3000/auth/callback"

    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@aeroelite.com"

    # Feature Flags
    ENABLE_PUBLIC_MODELS: bool = True
    ENABLE_PHYSICS_VALIDATION: bool = True
    ENABLE_ASSEMBLY_CHECKING: bool = True
    ENABLE_CONTINUOUS_LEARNING: bool = True

    # Dataset URLs
    AIRCRAFTVERSE_URL: str = "https://zenodo.org/records/6525446"
    G2AERO_URL: str = "https://data.openei.org/submissions/6198"
    NASA_CRM_URL: str = "https://commonresearchmodel.larc.nasa.gov/"

    # Privacy & Billing
    PRIVATE_MODEL_MONTHLY_COST: float = 9.99
    STORAGE_COST_PER_GB: float = 0.02

    # CAD Settings
    MAX_MODEL_SIZE_MB: int = 500
    SUPPORTED_EXPORT_FORMATS: List[str] = ["step", "iges", "stl", "obj", "gltf"]

    # AI Model Settings
    GEMINI_MODEL: str = "gemini-1.5-pro"
    VERTEX_AI_MODEL: str = "text-bison@002"
    EMBEDDING_MODEL: str = "textembedding-gecko@003"
    MAX_TOKENS: int = 8192
    TEMPERATURE: float = 0.7

    # Physics Validation Thresholds
    MIN_LIFT_COEFFICIENT: float = 0.2
    MAX_STRESS_MPA: float = 400.0
    MAX_DEFLECTION_MM: float = 100.0
    SAFETY_FACTOR: float = 1.5

    # Assembly Tolerances
    ASSEMBLY_TOLERANCE_MM: float = 0.1
    INTERFERENCE_CHECK_RESOLUTION: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings"""
    return Settings()


settings = get_settings()

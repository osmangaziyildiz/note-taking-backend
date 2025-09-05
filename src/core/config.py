import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Firebase Configuration
    FIREBASE_SERVICE_ACCOUNT_KEY_PATH: str = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH", "./serviceAccountKey.json")
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "")
    
    # App Settings
    APP_NAME: str = os.getenv("APP_NAME", "Notes API")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./notes.db")
    
    @property
    def firebase_credentials_path(self) -> Path:
        return Path(self.FIREBASE_SERVICE_ACCOUNT_KEY_PATH).resolve()

    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings()

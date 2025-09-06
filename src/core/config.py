import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Firebase Configuration
    FIREBASE_SERVICE_ACCOUNT_KEY_PATH: str = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH", "./serviceAccountKey.json")
    FIREBASE_SERVICE_ACCOUNT_KEY: str = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY", "")
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
    
    @property
    def firebase_credentials_dict(self) -> dict:
        """Get Firebase credentials as dictionary from environment variable."""
        if self.FIREBASE_SERVICE_ACCOUNT_KEY:
            import json
            return json.loads(self.FIREBASE_SERVICE_ACCOUNT_KEY)
        return None

    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings()

from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite:///data/gst_billing.db"
    secret_key: str = "dev-secret-key-change-in-production"
    session_secret: str = "dev-session-secret-change-in-production"
    storage_path: str = "storage"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:5173,http://localhost:3000,http://localhost:4173"
    
    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]
    
    @property
    def db_path(self) -> Path:
        return Path(self.database_url.replace("sqlite:///", ""))
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
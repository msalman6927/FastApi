# taskmanager/config.py  -- settings from .env (Day 21)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Task Manager API"
    jwt_secret: str = "dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    token_minutes: int = 30
    database_url: str = "sqlite:///tasks.db"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

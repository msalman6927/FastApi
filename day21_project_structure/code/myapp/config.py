# myapp/config.py
# -----------------------------------------------------------
# Central configuration loaded from a .env file, validated by Pydantic.
# Import `settings` anywhere: `from .config import settings`.
#
# SETUP: pip install pydantic-settings
# -----------------------------------------------------------

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # These come from environment variables or the .env file.
    app_name: str = "My App"
    jwt_secret: str = "dev-secret-change-me"   # override in .env for real use
    database_url: str = "sqlite:///app.db"
    debug: bool = False

    # Tell pydantic-settings to read a .env file (if present).
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Create ONE settings instance and import it everywhere (don't re-create it).
settings = Settings()

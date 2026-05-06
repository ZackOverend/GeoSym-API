from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = Field(default=..., validation_alias="DATABASE_URL")
    debug: bool = False
    upload_dir: Path = BASE_DIR / "uploads"


settings = Settings()

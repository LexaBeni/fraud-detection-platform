from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[3]
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=False)


class Settings(BaseSettings):
    model_path: str = ""
    database_url: str = ""
    admin_email: str = ""
    admin_password: str = ""
    jwt_secret_key: str = ""
    jwt_algorithm: str = ""
    access_token_expires_minutes: int = 1
    refresh_token_expires_days: int = 1

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()

if not settings.database_url:
    raise RuntimeError(
        f"DATABASE_URL is not configured."
    )
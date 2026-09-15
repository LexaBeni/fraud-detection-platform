from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "fraud_detection_model.joblib"


class Settings(BaseSettings):
    model_path: str = str(DEFAULT_MODEL_PATH)
    database_url: str = ""
    admin_email: str = ""
    admin_password: str = ""
    jwt_secret_key: str = ""
    jwt_algorithm: str = ""
    access_token_expires_minutes: int = 1
    refresh_token_expires_days: int = 1
    test_database_url: str = ""
    database_server_url: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()

if settings.model_path and not Path(settings.model_path).is_absolute():
    settings.model_path = str(PROJECT_ROOT / settings.model_path)

if not settings.database_url:
    raise RuntimeError("DATABASE_URL is not configured.")

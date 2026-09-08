from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_path: str = ""
    database_url: str = ""
    admin_email: str = ""
    admin_password: str = ""
    jwt_secret_key: str = ""
    jwt_algorithm: str = ""
    access_token_expires_minutes: int = 1
    refresh_token_expires_days: int = 1
    test_database_url: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()

if not settings.database_url:
    raise RuntimeError(
        f"DATABASE_URL is not configured."
    )
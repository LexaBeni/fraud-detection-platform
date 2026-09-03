from datetime import datetime, timedelta, timezone
from jose import jwt
from src.api.core.settings import settings

class TokenService:

    @staticmethod
    def create_token(data: dict, exp_delta: timedelta):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + exp_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, settings.jwt_algorithm)

        return encoded_jwt

    @staticmethod
    def create_access_token(user):
        return TokenService.create_token({"sub": str(user.id), "type": "access"}, exp_delta = timedelta(minutes=settings.access_token_expires_minutes))

    @staticmethod
    def create_refresh_token(user):
        return TokenService.create_token({"sub": str(user.id), "type": "refresh"}, exp_delta=timedelta(days=settings.refresh_token_expires_days))
    
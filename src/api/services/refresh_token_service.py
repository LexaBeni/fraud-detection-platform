from sqlalchemy.orm import Session
from src.api.core.security import hash_token
from src.api.models.refresh_token import RefreshToken
from src.api.services.token_service import TokenData
from sqlalchemy import select
from datetime import datetime, timezone
from src.api.core.exceptions import InvalidRefreshToken


class RefreshTokenService:
    def __init__(self, db: Session):
        self.db = db

    def append_refresh_token(self, refresh_token, user):

        refresh_token_db = RefreshToken(
            user_id = user.id,
            token_hash = hash_token(refresh_token.token),
            expires_at = refresh_token.expires_at                              
        )
        self.db.add(refresh_token_db)
        self.db.commit()
        self.db.refresh(refresh_token_db)

        return refresh_token_db

    def get_refresh_token(self, refresh_token: str):
        hashed_token = hash_token(refresh_token)

        stmt = select(RefreshToken).where(RefreshToken.token_hash == hashed_token)

        result = self.db.execute(stmt).scalar_one_or_none()

        if not result:
            InvalidRefreshToken()

        if result.revoked:
            InvalidRefreshToken()

        if result.expires_at < datetime.now(timezone.utc):
            InvalidRefreshToken()

        return result

    def revoke_refresh_token(self, refresh_token_db):
        refresh_token_db.revoked = True
        self.db.commit()

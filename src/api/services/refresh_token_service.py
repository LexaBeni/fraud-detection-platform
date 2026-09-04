from sqlalchemy.orm import Session
from src.api.core.security import hash_token
from src.api.models.refresh_token import RefreshToken


class RefreshTokenService:
    def __init__(self, db: Session):
        self.db = db

    def append_refresh_token(self, data, user):

        refresh_token_db = RefreshToken(
            user_id = user.id,
            token_hash = hash_token(data.token),
            expires_at = data.expires_at                              
        )
        self.db.add(refresh_token_db)
        self.db.commit()
        self.db.refresh(refresh_token_db)

        return refresh_token_db

from __future__ import annotations

from src.api.core.database import Base
from datetime import datetime
from sqlalchemy import Boolean, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.api.models.user import User

class RefreshToken(Base):

    __tablename__ = "refresh_tokens"

    id: Mapped[str] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    token_hash: Mapped[str] = mapped_column(
        String(128), nullable=False, unique=True
    )

    exprires_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )

    revoked: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")
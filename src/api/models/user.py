from __future__ import annotations

from src.api.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import DateTime, String, Integer, Boolean
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.api.models.prediction import Prediction

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    email: Mapped[str] = mapped_column(
        String(70), nullable=False, unique=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(25), default="user"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default = datetime.utcnow()
    )

    predictions: Mapped[list["Prediction"]] = relationship(back_populates="user")

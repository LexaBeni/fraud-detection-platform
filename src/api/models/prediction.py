from __future__ import annotations

from src.api.core.database import Base
from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from src.api.models.user import User

class Prediction(Base):

    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    transaction_id: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        index=True
    )

    prediction_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    prediction: Mapped[int] = mapped_column(
            Integer,
            nullable=False
        )

    label: Mapped[Literal["FRAUD", 'VALID']] = mapped_column(
        String(10),
        nullable=False
    )

    threshold: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow(),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    user: Mapped["User"] = relationship(back_populates="predictions")

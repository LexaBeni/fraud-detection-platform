from core.database import Base
from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

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

    threshold: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow(),
        nullable=False
    )
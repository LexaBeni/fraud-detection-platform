from src.api.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import DateTime, String, Integer, Boolean
from datetime import datetime

class User(Base):

    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    email: Mapped[str] = mapped_column(
        String(70), nullable=False, unique=True
    )

    hushed_password: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(25), default="user"
    )

    is_active: Mapped[str] = mapped_column(
        Boolean, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default = datetime.utcnow()
    )
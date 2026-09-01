from sqlalchemy import select
from sqlalchemy.orm import Session
from src.api.models.user import User
from src.api.core.settings import settings
from src.api.core.security import hash_password
from src.roles import UserRole

def ensure_admin(db: Session):
    stmt = select(User).where(User.role == "admin")
    admin = db.execute(stmt)
    admin = admin.scalar_one_or_none()

    if not admin:
        admin_db = User(
            email=settings.admin_email,
            hashed_password = hash_password(settings.admin_password),
            role = UserRole.ADMIN,
        ) 

        db.add(admin_db)
        db.commit()
        db.refresh(admin_db)

        return admin_db

    return admin
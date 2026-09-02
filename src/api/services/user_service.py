from src.api.models.user import User
from sqlalchemy import select
from src.api.core.exceptions import UserAlreadyExists, InvalidCredentials
from src.api.core.security import hash_password, verify_password

class UserService:

    def __init__(self, db):
        self.db = db

    def get_user_by_email(self, email):
        stmt = select(User).where(User.email == email)
        result = self.db.execute(stmt)
        result = result.scalar_one_or_none()

        return result

    def get_user_by_id(self, id):
        stmt = select(User).where(User.id == id)
        result = self.db.execute(stmt).scalar_one_or_none()

        return result

    def register_user(self, user):
        if self.get_user_by_email(user.email):
            raise UserAlreadyExists(user.email)

        password = hash_password(user.password)

        user_db = User(
            email=user.email,
            hashed_password=password
        )

        self.db.add(user_db)
        self.db.commit()
        self.db.refresh(user_db)

        return user_db

    def login_user(self, user):

        user_db = self.get_user_by_email(user.email)

        if not user_db:
            raise InvalidCredentials()

        if not verify_password(user_db.hashed_password, user.password):
            raise InvalidCredentials()

        return user_db
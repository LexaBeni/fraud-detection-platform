from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.dependencies.database import get_db
from src.api.services.user_service import UserService
from src.api.schemas.user import UserCreate, UserResponse
from src.api.schemas.auth import TokenResponse
from fastapi.security import OAuth2PasswordRequestForm
from src.dependencies.auth import get_current_user
from src.api.models.user import User
from src.api.services.token_service import TokenService

router = APIRouter(prefix="/auth", tags=["User"])

@router.get("/me", response_model=TokenResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db=db)

    return service.register_user(user)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), user = UserCreate):
    service = UserService(db=db)

    user = UserCreate(email=data.username, password=data.password)

    user_db = service.login_user(user)

    access_token = TokenService.create_access_token(user_db)
    refresh_token = TokenService.create_refresh_token(user_db)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )



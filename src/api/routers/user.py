from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.dependencies.database import get_db
from src.api.services.user_service import UserService
from src.api.schemas.user import UserCreate, UserResponse
from src.api.schemas.auth import TokenResponse, RefreshTokenRequest
from fastapi.security import OAuth2PasswordRequestForm
from src.dependencies.auth import get_current_user, decode_refresh_token
from src.api.models.user import User
from src.api.services.token_service import TokenService
from src.api.services.refresh_token_service import RefreshTokenService
from src.api.core.exceptions import InvalidRefreshToken

router = APIRouter(prefix="/auth", tags=["User"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db=db)

    return service.register_user(user)

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    service = UserService(db=db)

    user = UserCreate(email=data.username, password=data.password)

    user_db = service.login_user(user)

    access_token = TokenService.create_access_token(user_db)
    refresh_token = TokenService.create_refresh_token(user_db)

    refresh_token_service = RefreshTokenService(db)
    
    refresh_token_service.append_refresh_token(refresh_token=refresh_token, user=user_db)

    db.commit()

    return TokenResponse(
        access_token=access_token.token,
        refresh_token=refresh_token.token
    )

@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        refresh_token = data.refresh_token

        payload = decode_refresh_token(refresh_token)

        user_service = UserService(db)

        user_id = payload['sub']

        user = user_service.get_user_by_id(int(user_id))

        if user is None or not user.is_active:
            raise InvalidRefreshToken()

        refresh_token_service = RefreshTokenService(db)

        refresh_token_db = refresh_token_service.get_refresh_token(refresh_token=refresh_token)

        if refresh_token_db.user_id != user.id:
            raise InvalidRefreshToken()

        refresh_token_service.revoke_refresh_token(refresh_token_db)

        new_access_token = TokenService.create_access_token(user)
        new_refresh_token = TokenService.create_refresh_token(user)

        refresh_token_service.append_refresh_token(refresh_token=new_refresh_token, user=user)

        db.commit()

        return TokenResponse(
            access_token=new_access_token.token,
            refresh_token=new_refresh_token.token
            )

    except Exception:
        db.rollback()
        raise

@router.post("/logout")
def logout(data: RefreshTokenRequest, db:Session = Depends(get_db)):
    service = RefreshTokenService(db=db)

    try:
        refresh_token = data.refresh_token

        payload = decode_refresh_token(refresh_token)

        refresh_token_db = service.get_refresh_token(refresh_token)

        if refresh_token_db.user_id != int(payload["sub"]):
            raise InvalidRefreshToken()

        service.revoke_refresh_token(refresh_token_db)

        db.commit()

        return f"The user with id {payload["sub"]} was successfully logged out!"
    
    except Exception:
        db.rollback()
        raise
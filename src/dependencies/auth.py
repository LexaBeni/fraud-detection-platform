from src.dependencies.database import get_db
from src.api.core.settings import settings
from src.api.core.security import oauth2_scheme
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWEError
from src.api.core.exceptions import InvalidCredentials

def decode_token(token: str):
    try:
        payload = jwt.decode(token=token, key=settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        sub = payload.get("sub")
        if not sub:
            raise InvalidCredentials()
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

    except JWEError:
        raise InvalidCredentials()
    
    except Exception:
        raise InvalidCredentials()

    return payload

def decode_access_token(token: str):
    payload = decode_token(token)

    token_type = payload.get("type")

    if token_type != "access":
        raise InvalidCredentials()

    return payload

def decode_refresh_token(token:str):

    payload = decode_token(token)

    if payload.get("type") != "refresh":
        raise InvalidCredentials()

    return payload

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from src.api.services.user_service import UserService

    service = UserService(db=db)

    payload = decode_access_token(token)

    user = service.get_user_by_id(payload["sub"])

    if user is None:
        raise InvalidCredentials()

    if not user.is_active:
        raise InvalidCredentials()

    return user
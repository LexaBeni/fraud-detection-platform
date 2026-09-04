from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import hashlib

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated="auto"
)

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_passowod):
    return pwd_context.verify(plain_password, hashed_passowod)

def hash_token(token: str):
    return hashlib.sha256(token.encode()).hexdigest()
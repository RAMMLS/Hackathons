from datetime import datetime, timedelta
from jose import JWTError, jwt
import hashlib
import secrets
from app.config import settings

# Простой хешер на основе SHA-256 (альтернатива bcrypt)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # Добавляем соль из хешированного пароля
        salt = hashed_password[:32]
        new_hash = hash_password_with_salt(plain_password, salt)
        return new_hash == hashed_password
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    # Генерируем случайную соль
    salt = secrets.token_hex(16)
    return hash_password_with_salt(password, salt)

def hash_password_with_salt(password: str, salt: str) -> str:
    # Хешируем пароль с солью
    return salt + hashlib.sha256((salt + password).encode()).hexdigest()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None
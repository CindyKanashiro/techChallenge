from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from fastapi import HTTPException, status
from passlib.context import CryptContext
import jwt

from settings import (
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ADMIN_PASSWORD,
    ADMIN_EMAIL,
)


def verify_password(plain_password, hashed_password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


def check_user_is_admin(username: str, password: str) -> bool:
    if username == ADMIN_EMAIL and verify_password(password, ADMIN_PASSWORD):
        return True


def sign_jwt(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Cria um token de acesso
    """
    payload = data.copy()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + access_token_expires
    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def refresh_token_jwt(token: str):
    """
    Irá renovar o token de acesso
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        payload.update({"exp": expire})
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

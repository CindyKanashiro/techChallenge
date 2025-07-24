from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import Annotated
from fastapi import Depends, HTTPException
from api.core.settings import ADMIN_EMAIL, ADMIN_PASSWORD
from api.core.auth.token import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def require_admin(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_token(token)
    if payload.get("sub") != ADMIN_EMAIL:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action",
        )

    return "OK"


def authenticate_admin(username: str, password: str) -> bool:
    if username != ADMIN_EMAIL:
        print("admin:")
        print(username)
        print(ADMIN_EMAIL)
    if not _verify_password(password, ADMIN_PASSWORD):
        print("password:")
        print(password)
        print(ADMIN_PASSWORD)
    if username == ADMIN_EMAIL and _verify_password(password, ADMIN_PASSWORD):
        return True
    return False


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

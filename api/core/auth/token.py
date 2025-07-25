from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException

from api.core.settings import (
    ACCESS_TOKEN_EXPIRE_TIME,
    ACCESS_TOKEN_REFRESH_TIME,
    ADMIN_EMAIL,
    ALGORITHM,
    SECRET_KEY,
)


def create_access_token() -> str:
    return _encode({"sub": ADMIN_EMAIL}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME))


def refresh_access_token(token: str) -> str:
    try:
        payload = decode_token(token)
        new_expire = timedelta(minutes=ACCESS_TOKEN_REFRESH_TIME)
        return _encode(payload, new_expire)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )


def _encode(payload: dict, ttl: timedelta) -> str:
    payload = payload.copy()
    payload["exp"] = _utc_now() + ttl
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)

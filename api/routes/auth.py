from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from settings import ADMIN_EMAIL
from auth.auth_handler import check_user_is_admin, sign_jwt, refresh_token_jwt
from auth.model import Token

from dotenv import load_dotenv

load_dotenv(".env")

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/login", tags=["Auth"])
async def get_jwt_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    is_admin = check_user_is_admin(form_data.username, form_data.password)
    if is_admin:
        access_token = sign_jwt(data={"sub": ADMIN_EMAIL})
        return Token(access_token=access_token, token_type="bearer")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/refresh", tags=["Auth"])
async def get_jwt_token(token: Annotated[str, Depends(oauth2_scheme)]) -> Token:
    access_token = refresh_token_jwt(token)
    return Token(access_token=access_token, token_type="Bearer")

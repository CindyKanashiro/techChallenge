from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api.auth.auth_handler import check_user_is_admin, refresh_token_jwt, sign_jwt
from api.auth.model import Token
from api.core.settings import ADMIN_EMAIL

load_dotenv(".env")

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/login")
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


@router.post("/refresh")
async def get_jwt_token(token: Annotated[str, Depends(oauth2_scheme)]) -> Token:
    access_token = refresh_token_jwt(token)
    return Token(access_token=access_token, token_type="Bearer")

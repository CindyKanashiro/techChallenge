from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from settings import ACCESS_TOKEN_EXPIRE_MINUTES
from auth.auth_handler import check_user, get_current_active_user, sign_jwt
from auth.model import *

from dotenv import load_dotenv

load_dotenv('.env')

router = APIRouter()


@router.post("/login", tags=["Auth"])
async def create_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    breakpoint()
    user = check_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = sign_jwt(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
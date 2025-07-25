from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api.core.auth import authenticate_admin, create_access_token, refresh_access_token
from api.schemas.auth import TokenSchema

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post(
    "/login",
    response_model=TokenSchema,
    summary="Login",
    description="Realiza o login do usuário e retorna um token de acesso.",
)
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenSchema:
    if not authenticate_admin(form_data.username, form_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return TokenSchema(access_token=create_access_token(), token_type="bearer")


@router.post(
    "/refresh",
    response_model=TokenSchema,
    summary="Renovar o token de acesso",
    description="Renova o token de acesso usando o token de atualização.",
)
def refresh(token: str = Depends(oauth2_scheme)) -> TokenSchema:
    token = refresh_access_token(token)
    return TokenSchema(access_token=token, token_type="bearer")

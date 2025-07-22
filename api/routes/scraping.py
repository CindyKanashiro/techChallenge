from typing import Annotated

from api.auth.auth_handler import check_user_is_authenticate
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.post("/trigger")
def start_scrapping(token: Annotated[str, Depends(check_user_is_authenticate)]):
    return {"Status": "Searching..."}

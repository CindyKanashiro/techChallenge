from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from auth.auth_handler import check_user_is_authenticate


router = APIRouter()


@router.post('/trigger')
def start_scrapping(
    token: Annotated[str, Depends(check_user_is_authenticate)]
):
    return {
        "Status": "Searching..."
    }
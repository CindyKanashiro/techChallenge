from fastapi import APIRouter, Depends

from api.core.auth import require_admin

router = APIRouter()


@router.post("/trigger")
def start_scrapping(_: str = Depends(require_admin)):
    return {"Status": "Searching..."}

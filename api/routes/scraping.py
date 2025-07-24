from fastapi import APIRouter, Depends, HTTPException
from scraping import download_catalogue_data
from api.core.auth import require_admin

router = APIRouter()


@router.post("/trigger")
def start_scrapping(_: str = Depends(require_admin)):
    try:
        download_catalogue_data()
        return {"message": "Scraping executed successfully."}
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while executing the scraping.",
        )

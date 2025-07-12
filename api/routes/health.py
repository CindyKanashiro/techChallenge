from fastapi import APIRouter
from api.db import get_metrics_summary, get_metrics_detailed

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "database": "connected",
        "message": "API is healthy"
    }

@router.get("/metrics", tags=["Health"])
async def metrics():
    return get_metrics_summary()

@router.get("/metrics/detailed", tags=["Health"])
async def metrics_detailed():
    return get_metrics_detailed(limit=100)

from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from api.core.database import get_books_session, get_logs_session

router = APIRouter(prefix="/api/v1/health", tags=["Health"])


@router.get(
    "",
    response_model=dict[str, str],
    summary="Health Check",
    description="Checa a disponibilidade dos bancos de dados.",
)
def get_health_check() -> dict[str, str]:
    books_db = get_books_session()
    logs_db = get_logs_session()

    books_db_status = _check_database_connection(books_db)
    logs_db_status = _check_database_connection(logs_db)

    failed_dbs = []

    if not books_db_status:
        failed_dbs.append("books")
    if not logs_db_status:
        failed_dbs.append("logs")

    if len(failed_dbs) > 0:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed for: {', '.join(failed_dbs)}",
        )
    return {"status": "ok", "message": "All databases are reachable."}


def _check_database_connection(db: Session) -> bool:
    try:
        db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
    finally:
        db.close()

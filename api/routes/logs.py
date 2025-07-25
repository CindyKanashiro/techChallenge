from typing import Optional

from fastapi import APIRouter

from api.core.database import get_logs_session
from api.models.logs import AppLogModel, RequestLogModel
from api.schemas.logs import AppLogSchema, RequestLogSchema

router = APIRouter(prefix="/log", tags=["Log"])


@router.get(
    "/app",
    response_model=list[AppLogSchema],
    summary="Listar logs da aplicação",
    description="Retorna uma lista de logs da aplicação.",
)
def list_app_logs(
    limit: Optional[int] = None,
    filename: Optional[str] = None,
    level: Optional[str] = None,
    min_timestamp: float = None,
    max_timestamp: float = None,
) -> list[AppLogSchema]:
    db = get_logs_session()
    try:
        query = db.query(AppLogModel).order_by(AppLogModel.ts.desc())
        if min_timestamp:
            query = query.filter(AppLogModel.ts >= min_timestamp)
        if max_timestamp:
            query = query.filter(AppLogModel.ts <= max_timestamp)
        if filename:
            query = query.filter(AppLogModel.filename == filename)
        if level:
            query = query.filter(AppLogModel.level == level)
        if limit:
            query = query.limit(limit)
        return list(map(AppLogSchema.model_validate, query.all()))
    finally:
        db.close()


@router.get(
    "/requests",
    response_model=list[RequestLogSchema],
    summary="Listar logs de requisições",
    description="Retorna uma lista de logs de requisições.",
)
def list_request_logs(
    limit: Optional[int] = None,
    method: Optional[str] = None,
    status_code: Optional[int] = None,
    min_timestamp: float = None,
    max_timestamp: float = None,
) -> list[RequestLogSchema]:
    db = get_logs_session()
    try:
        query = db.query(RequestLogModel).order_by(RequestLogModel.ts.desc())
        if min_timestamp:
            query = query.filter(RequestLogModel.ts >= min_timestamp)
        if max_timestamp:
            query = query.filter(RequestLogModel.ts <= max_timestamp)
        if method:
            query = query.filter(RequestLogModel.method == method)
        if status_code:
            query = query.filter(RequestLogModel.status_code == status_code)
        if limit:
            query = query.limit(limit)
        return list(map(RequestLogSchema.model_validate, query.all()))
    finally:
        db.close()


@router.get(
    "/requests/stats",
    response_model=dict,
    summary="Estatísticas de requisições",
    description="Retorna estatísticas sobre as requisições.",
)
def get_requests_statistics(
    method: Optional[str] = None,
    min_timestamp: Optional[float] = None,
    max_timestamp: Optional[float] = None,
) -> dict:
    db = get_logs_session()
    try:
        query = db.query(RequestLogModel)
        if min_timestamp:
            query = query.filter(RequestLogModel.ts >= min_timestamp)
        if max_timestamp:
            query = query.filter(RequestLogModel.ts <= max_timestamp)
        if method:
            query = query.filter(RequestLogModel.method == method)

        total_requests = query.count()
        successful_requests = query.filter(
            RequestLogModel.status_code >= 200, RequestLogModel.status_code < 300
        ).count()
        failed_requests = total_requests - successful_requests

        return {
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
        }
    finally:
        db.close()

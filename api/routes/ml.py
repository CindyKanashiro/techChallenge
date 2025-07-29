from fastapi import APIRouter
from api.core.database import get_books_session
from api.models.books import BookModel
from api.schemas.books import BookSchema

router = APIRouter(prefix="/api/v1/ml", tags=["Machine-Learning"])


@router.get(
    "/features",
    response_model=list[BookSchema],
    summary="Features",
    description="Retorna features do dataset.",
)
def get_features() -> list[BookSchema]:
    db = get_books_session()

    try:
        return list(map(BookSchema.model_validate, db.query(BookModel).all()))
    finally:
        db.close()


@router.get(
    "/training-data",
    response_model=list[BookSchema],
    summary="Training Data",
    description="Dataset de treinamento para o modelo.",
)
def get_training_data() -> list[BookSchema]:
    db = get_books_session()

    try:
        return list(map(BookSchema.model_validate, db.query(BookModel).all()))
    finally:
        db.close()

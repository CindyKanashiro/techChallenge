from fastapi import APIRouter

from api.core.database import get_books_session
from api.models.books import BookModel

router = APIRouter(prefix="/api/v1/categories", tags=["Categories"])


@router.get(
    "",
    response_model=list[str],
    summary="Listar categorias",
    description="Retorna uma lista de todas as categorias de livros.",
)
def list_categories() -> list[str]:
    db = get_books_session()

    try:
        query = (
            db.query(BookModel.category).distinct().order_by(BookModel.category.asc())
        )
        return [row[0] for row in query.all()]
    finally:
        db.close()

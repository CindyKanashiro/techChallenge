from fastapi import APIRouter, HTTPException # type: ignore
from collections import defaultdict
from pydantic import BaseModel  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.exc import OperationalError  # type: ignore
from database import SessionLocal  # type: ignore
from models import BookORM  # type: ignore

router = APIRouter(
    prefix="/api/v1/categories",
    tags=["categories"]
)


class BookWithCategory(BaseModel):
    id: int
    title: str
    price: float
    rating: int
    category: str


@router.get(
    "/stats",
    summary="Estatísticas por categoria",
    description="Retorna estatísticas agregadas de livros por categoria.",
)
def stats_by_category():
    """
    Estatísticas agregadas de livros por categoria.

    - **quantidade**: número de livros na categoria
    - **preço total**: soma dos preços dos livros na categoria
    - **média de preço**: média dos preços dos livros na categoria
    """
    db: Session = SessionLocal()
    try:
        books = db.query(BookORM).all()
    except OperationalError:
        db.close()
        raise HTTPException(
            status_code=500,
            detail="Tabela de livros não existe no banco de dados."
        )
    if not books:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Nenhum livro cadastrado no banco de dados."
        )
    category_stats = defaultdict(
        lambda: {"quantidade": 0, "preço total": 0.0, "média de preço": 0.0}
    )
    for book in books:
        cat = book.category
        category_stats[cat]["quantidade"] += 1
        category_stats[cat]["preço total"] += book.price
    # Calcular média de preço por categoria
    for cat in category_stats:
        count = category_stats[cat]["quantidade"]
        total = category_stats[cat]["preço total"]
        category_stats[cat]["média de preço"] = total / count if count > 0 else 0
    db.close()
    return category_stats

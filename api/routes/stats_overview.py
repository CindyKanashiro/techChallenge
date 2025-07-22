from collections import Counter
from typing import Dict

from api.database import SessionLocal
from api.models import BookORM
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/stats", tags=["overview"])


class Book(BaseModel):
    id: int
    title: str
    price: float
    rating: int


@router.get(
    "/overview",
    summary="Estatísticas gerais dos livros",
    description="Retorna estatísticas gerais dos livros, incluindo total de livros, média de preço e distribuição de ratings.",
    response_description="Estatísticas gerais dos livros",
)
def stats_overview() -> Dict:
    """
    Estatísticas gerais dos livros.

    - **Total de Livros**: quantidade total de livros cadastrados
    - **Média de Preço**: média dos preços dos livros
    - **Distribuição de Ratings**: quantidade de livros por nota de avaliação
    """
    db: Session = SessionLocal()
    try:
        books = db.query(BookORM).all()
    except OperationalError:
        db.close()
        raise HTTPException(
            status_code=500, detail="Tabela de livros não existe no banco de dados."
        )
    total_books = len(books)
    if total_books == 0:
        db.close()
        raise HTTPException(
            status_code=404, detail="Nenhum livro cadastrado no banco de dados."
        )
    avg_price = (
        sum(book.price for book in books) / total_books if total_books > 0 else 0
    )
    ratings = [book.rating for book in books]
    rating_distribution = dict(Counter(ratings))
    db.close()
    return {
        "Total de Livros": total_books,
        "Média de Preço": avg_price,
        "Distribuição de Ratings": rating_distribution,
    }

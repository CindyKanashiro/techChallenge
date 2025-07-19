from fastapi import APIRouter, HTTPException  
from pydantic import BaseModel  
from typing import List
from sqlalchemy.orm import Session  
from sqlalchemy.exc import OperationalError  
from database import SessionLocal  
from models import BookORM  

router = APIRouter(  
    prefix="/api/v1/books",
    tags=["top-rated"]
)

class Book(BaseModel):
    id: int
    title: str
    price: float
    rating: int
    category: str

@router.get(
    "/top-rated",
    response_model=List[Book],
    summary="Buscar livros com maior avaliação",
    description="Retorna uma lista dos 10 livros com a maior nota de avaliação.",
    response_description="Lista dos 10 livros com maior avaliação"
)
def get_top_rated_books():
    """
    Busca os 10 livros com maior avaliação.

    - Retorna: lista dos 10 livros com nota de avaliação maior entre todos os livros cadastrados.
    """
    db: Session = SessionLocal()
    try:
        books = db.query(BookORM).order_by(BookORM.rating.desc(), BookORM.id.asc()).limit(10).all()
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
            detail="Nenhum livro encontrado para avaliação."
        )
    result = [
        Book(
            id=book.id,
            title=book.title,
            price=book.price,
            rating=book.rating,
            category=book.category,
        )
        for book in books
    ]
    db.close()
    return result

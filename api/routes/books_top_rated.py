from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel  # type: ignore
from typing import List
from sqlalchemy import Column, Integer, String, Float  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.exc import OperationalError  # type: ignore
from database import SessionLocal, Base

app = FastAPI(
    title="Book Top Rated API",
    description="API para buscar livros com maior avaliação.",
    version="1.0.0"
)


class BookORM(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    price = Column(Float)
    rating = Column(Integer)
    category = Column(String)


class Book(BaseModel):
    id: int
    title: str
    price: float
    rating: int
    category: str


@app.get(
    "/api/v1/books/top-rated",
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

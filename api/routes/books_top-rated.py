from fastapi import FastAPI  # type: ignore
from pydantic import BaseModel  # type: ignore
from typing import List
from sqlalchemy import Column, Integer, String, Float  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
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
    description="Retorna uma lista de livros com a maior nota de avaliação.",
    response_description="Lista de livros com maior avaliação"
)
def get_top_rated_books():
    """
    Busca livros com maior avaliação.

    - Retorna: lista de livros com nota de avaliação maior entre todos os livros cadastrados.
    """
    db: Session = SessionLocal()
    books = db.query(BookORM).all()
    if not books:
        db.close()
        return []
    max_rating = max(book.rating for book in books)
    top_books = [
        Book(
            id=book.id,
            title=book.title,
            price=book.price,
            rating=book.rating,
            category=book.category,
        )
        for book in books if book.rating == max_rating
    ]
    db.close()
    return top_books

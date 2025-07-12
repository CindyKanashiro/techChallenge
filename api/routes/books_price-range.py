from fastapi import FastAPI, Query  # type: ignore
from pydantic import BaseModel  # type: ignore
from typing import List
from sqlalchemy import Column, Integer, String, Float  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from database import SessionLocal, Base

app = FastAPI(
    title="Book Price Range API",
    description="API para buscar livros por faixa de preço.",
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
    "/api/v1/books/price-range",
    response_model=List[Book],
    summary="Buscar livros por faixa de preço",
    description="Retorna uma lista de livros com preço entre os valores mínimo e máximo informados.",
    response_description="Lista de livros dentro da faixa de preço"
)
def get_books_by_price_range(
    min: float = Query(..., description="Preço mínimo", gt=0),
    max: float = Query(..., description="Preço máximo", gt=0)
):
    """
    Busca livros por faixa de preço.

    - **min**: preço mínimo (float, obrigatório)
    - **max**: preço máximo (float, obrigatório)
    - Retorna: lista de livros com preço entre min e max
    """
    db: Session = SessionLocal()
    books = db.query(BookORM).filter(BookORM.price >= min, BookORM.price <= max).all()
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

from fastapi import FastAPI # type: ignore
from typing import Dict
from pydantic import BaseModel # type: ignore
from collections import Counter
from sqlalchemy import Column, Integer, String, Float # type: ignore
from sqlalchemy.orm import Session # type: ignore
from database import SessionLocal, Base

app = FastAPI()

# Modelo ORM
class BookORM(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    price = Column(Float)
    rating = Column(Integer)
    category = Column(String)

# Modelo Pydantic
class Book(BaseModel):
    id: int
    title: str
    price: float
    rating: int  # Exemplo: 1 a 5

@app.get("/api/v1/stats/overview")
def stats_overview() -> Dict:
    db: Session = SessionLocal()
    books = db.query(BookORM).all()
    total_books = len(books)
    avg_price = sum(book.price for book in books) / total_books if total_books > 0 else 0
    ratings = [book.rating for book in books]
    rating_distribution = dict(Counter(ratings))
    db.close()
    return {
        "Total de Livros": total_books,
        "Média de Preço": avg_price,
        "Distribuição de Ratings": rating_distribution
    }
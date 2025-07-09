from fastapi import FastAPI # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List
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
    rating: int
    category: str

@app.get("/api/v1/books/top-rated", response_model=List[Book])
def get_top_rated_books():
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
            category=book.category
        )
        for book in books if book.rating == max_rating
    ]
    db.close()
    return top_books

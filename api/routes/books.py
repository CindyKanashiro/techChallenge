from fastapi import APIRouter, HTTPException
from models import Book
from database import books_db

router = APIRouter(prefix="/api/v1/books", tags=["Books"])


@router.get("/", response_model=list[Book])
def list_books():
    return books_db


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@router.get("/categories", response_model=list[str])
def list_categories():
    categories = list({book.category for book in books_db if book.category})
    return sorted(categories)

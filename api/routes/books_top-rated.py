from fastapi import FastAPI # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List

app = FastAPI()

# Modelo de Livro
class Book(BaseModel):
    id: int
    title: str
    price: float
    rating: int
    category: str

# Exemplo de coleção de livros
books_db = [
    Book(id=1, title="Livro A", price=50.0, rating=4, category="Ficção"),
    Book(id=2, title="Livro B", price=70.0, rating=5, category="Ficção"),
    Book(id=3, title="Livro C", price=40.0, rating=3, category="Tecnologia"),
    Book(id=4, title="Livro D", price=60.0, rating=4, category="Tecnologia"),
    Book(id=5, title="Livro E", price=80.0, rating=5, category="Negócios"),
]

@app.get("/api/v1/books/top-rated", response_model=List[Book])
def get_top_rated_books():
    if not books_db:
        return []
    max_rating = max(book.rating for book in books_db)
    top_books = [book for book in books_db if book.rating == max_rating]
    return top_books

from fastapi import FastAPI # type: ignore
from typing import List, Dict
from pydantic import BaseModel # type: ignore
from collections import Counter

app = FastAPI()

# Modelo de Livro
class Book(BaseModel):
    id: int
    title: str
    price: float
    rating: int  # Exemplo: 1 a 5

# Exemplo de coleção de livros
books_db = [
    Book(id=1, title="Livro A", price=50.0, rating=4),
    Book(id=2, title="Livro B", price=70.0, rating=5),
    Book(id=3, title="Livro C", price=40.0, rating=3),
    Book(id=4, title="Livro D", price=60.0, rating=4),
]

@app.get("/api/v1/stats/overview")
def stats_overview():
    total_books = len(books_db)
    avg_price = sum(book.price for book in books_db) / total_books if total_books > 0 else 0
    ratings = [book.rating for book in books_db]
    rating_distribution = dict(Counter(ratings))
    return {
        "Total de Livros": total_books,
        "Média de Preço": avg_price,
        "Distribuição de Ratings": rating_distribution
    }
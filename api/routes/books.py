from fastapi import APIRouter, Query, HTTPException
from typing import Optional

router = APIRouter()

# Base de dados fictícia
fake_books = [
    {"id": 1, "title": "1984", "author": "George Orwell", "category": "Ficção", "year": 1949},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin", "category": "Tecnologia", "year": 2008},
    {"id": 3, "title": "O Senhor dos Anéis", "author": "J.R.R. Tolkien", "category": "Fantasia", "year": 1954},
    {"id": 4, "title": "Python Crash Course", "author": "Eric Matthes", "category": "Tecnologia", "year": 2019},
    {"id": 5, "title": "Dom Casmurro", "author": "Machado de Assis", "category": "Clássico", "year": 1899}
]

@router.get("/books/search", tags=["Books"])
def search_books(
    title: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    author: Optional[str] = Query(None)
):
    results = fake_books

    if title:
        results = [book for book in results if title.lower() in book["title"].lower()]
    if category:
        results = [book for book in results if category.lower() in book["category"].lower()]
    if author:
        results = [book for book in results if author.lower() in book["author"].lower()]

    if not results:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado.")

    return results

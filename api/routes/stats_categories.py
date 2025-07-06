from fastapi import FastAPI # type: ignore
from collections import defaultdict
from pydantic import BaseModel # type: ignore

app = FastAPI()

# Modelo de Livro com categoria
class BookWithCategory(BaseModel):
    id: int
    title: str
    price: float
    rating: int
    category: str

# Exemplo de coleção de livros com categoria
books_db = [
    BookWithCategory(id=1, title="Livro A", price=50.0, rating=4, category="Ficção"),
    BookWithCategory(id=2, title="Livro B", price=70.0, rating=5, category="Ficção"),
    BookWithCategory(id=3, title="Livro C", price=40.0, rating=3, category="Tecnologia"),
    BookWithCategory(id=4, title="Livro D", price=60.0, rating=4, category="Tecnologia"),
    BookWithCategory(id=5, title="Livro E", price=80.0, rating=5, category="Negócios"),
]

@app.get("/api/v1/stats/categories")
def stats_by_category():
    category_stats = defaultdict(lambda: {"quantidade": 0, "preço total": 0.0, "média de preço": 0.0})
    for book in books_db:
        cat = book.category
        category_stats[cat]["quantidade"] += 1
        category_stats[cat]["preço total"] += book.price
    # Calcular média de preço por categoria
    for cat in category_stats:
        count = category_stats[cat]["quantidade"]
        total = category_stats[cat]["preço total"]
        category_stats[cat]["média de preço"] = total / count if count > 0 else 0
    return category_stats

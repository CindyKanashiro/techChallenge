from fastapi import FastAPI  # type: ignore
from collections import defaultdict
from pydantic import BaseModel  # type: ignore
from sqlalchemy import Column, Integer, String, Float  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from database import SessionLocal, Base

app = FastAPI(
    title="Book Categories Stats API",
    description="API para estatísticas de livros por categoria.",
    version="1.0.0",
)


class BookORM(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    price = Column(Float)
    rating = Column(Integer)
    category = Column(String)


class BookWithCategory(BaseModel):
    id: int
    title: str
    price: float
    rating: int
    category: str


@app.get(
    "/api/v1/stats/categories",
    summary="Estatísticas por categoria",
    description="Retorna estatísticas agregadas de livros por categoria, incluindo quantidade, preço total e média de preço.",
    response_description="Estatísticas por categoria",
)
def stats_by_category():
    """
    Estatísticas agregadas de livros por categoria.

    - **quantidade**: número de livros na categoria
    - **preço total**: soma dos preços dos livros na categoria
    - **média de preço**: média dos preços dos livros na categoria
    """
    db: Session = SessionLocal()
    books = db.query(BookORM).all()
    category_stats = defaultdict(
        lambda: {"quantidade": 0, "preço total": 0.0, "média de preço": 0.0}
    )
    for book in books:
        cat = book.category
        category_stats[cat]["quantidade"] += 1
        category_stats[cat]["preço total"] += book.price
    # Calcular média de preço por categoria
    for cat in category_stats:
        count = category_stats[cat]["quantidade"]
        total = category_stats[cat]["preço total"]
        category_stats[cat]["média de preço"] = total / count if count > 0 else 0
    db.close()
    return category_stats

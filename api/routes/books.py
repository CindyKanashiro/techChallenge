from typing import Optional

from fastapi import APIRouter, HTTPException

from api.core.database import get_books_session
from api.models.books import BookModel
from api.schemas.books import BookSchema

router = APIRouter(prefix="/api/v1/books", tags=["Books"])


@router.get(
    "",
    response_model=list[BookSchema],
    summary="Listar livros",
    description="Retorna uma lista de livros com opções de filtragem.",
)
def list_books(
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    title: Optional[str] = None,
    category: Optional[str] = None,
) -> list[BookSchema]:
    db = get_books_session()

    try:
        query = db.query(BookModel)
        if title:
            query = query.filter(BookModel.title == title)
        if category:
            query = query.filter(BookModel.category == category)
        if skip:
            query = query.offset(skip)
        if limit:
            query = query.limit(limit)
        return list(map(BookSchema.model_validate, query.all()))
    finally:
        db.close()


@router.get(
    "/top-rated",
    response_model=list[BookSchema],
    summary="Listar livros mais bem avaliados",
    description="Retorna uma lista de livros ordenados por avaliação.",
)
def list_top_rated_books(
    skip: Optional[int] = None, limit: Optional[int] = 10
) -> list[BookSchema]:
    db = get_books_session()

    try:
        query = db.query(BookModel).order_by(BookModel.rating.desc())
        if skip:
            query = query.offset(skip)
        if limit:
            query = query.limit(limit)
        return list(map(BookSchema.model_validate, query.all()))
    finally:
        db.close()


@router.get(
    "/price-range",
    response_model=list[BookSchema],
    summary="Listar livros por faixa de preço",
    description="Retorna uma lista de livros filtrados por faixa de preço.",
)
def get_books_by_price_range(min: float, max: float) -> list[BookSchema]:
    db = get_books_session()

    try:
        query = db.query(BookModel).filter(
            BookModel.price >= min, BookModel.price <= max
        )
        return list(map(BookSchema.model_validate, query.all()))
    finally:
        db.close()


@router.get(
    "/{book_id}",
    response_model=BookSchema,
    summary="Obter livro por ID",
    description="Retorna os detalhes de um livro específico pelo ID.",
)
def get_book(book_id: int) -> BookSchema:
    db = get_books_session()

    try:
        book = db.query(BookModel).filter(BookModel.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return BookSchema.model_validate(book)
    finally:
        db.close()

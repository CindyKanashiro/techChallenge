from fastapi import APIRouter
from sqlalchemy import func

from api.core.database import get_books_session
from api.models.books import BookModel
from api.schemas.stats import (
    BooksSummarySchema,
    CategoriesSummarySchema,
    RatingsDistributionSchema,
)

router = APIRouter(prefix="/api/v1/stats", tags=["Stats"])


@router.get(
    "/overview",
    response_model=BooksSummarySchema,
    summary="Estatísticas gerais da base de livros",
    description=(
        "Retorna estatísticas gerais da base de livros, incluindo número "
        "total de livros, média de preço e distribuição de avaliações."
    ),
)
def get_books_summary() -> BooksSummarySchema:
    db = get_books_session()

    try:
        total_books = db.query(func.count(BookModel.id)).scalar()
        avg_price = db.query(func.avg(BookModel.price)).scalar()
        ratings = (
            db.query(
                BookModel.rating.label("rating"),
                func.count(BookModel.id).label("count"),
            )
            .group_by(BookModel.rating)
            .order_by(BookModel.rating)
            .all()
        )

        ratings = list(map(RatingsDistributionSchema.model_validate, ratings))

        return BooksSummarySchema(
            number_of_books=total_books,
            average_price=avg_price,
            rating_distribution=ratings,
        )
    finally:
        db.close()


@router.get(
    "/categories",
    response_model=list[CategoriesSummarySchema],
    summary="Estatísticas por categoria",
    description="Retorna estatísticas agregadas de livros por categoria.",
)
def get_categories_summary() -> list[CategoriesSummarySchema]:
    db = get_books_session()

    try:
        categories = (
            db.query(
                BookModel.category.label("category"),
                func.count(BookModel.id).label("number_of_books"),
                func.avg(BookModel.price).label("average_price"),
            )
            .group_by(BookModel.category)
            .order_by(BookModel.category)
            .all()
        )

        return list(map(CategoriesSummarySchema.model_validate, categories))
    finally:
        db.close()

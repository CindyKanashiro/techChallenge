from api.logger.setup import setup_logging
from fastapi import FastAPI

from api.routes import (
    books_price_range,
    books_top_rated,
    stats_categories,
    stats_overview,
)
from api.routes import auth, scraping
from api.routes.books import router as books_router

setup_logging("log.db")

app = FastAPI(title="Books API", version="1.0")

app.include_router(books_router)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(scraping.router, prefix="/scraping", tags=["Scraping"])
app.include_router(books_price_range.router)
app.include_router(books_top_rated.router)
app.include_router(stats_overview.router)
app.include_router(stats_categories.router)

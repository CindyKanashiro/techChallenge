from fastapi import FastAPI
from api.routes import books

app = FastAPI(
    title="Book Public API",
    version="1.0.0"
)

app.include_router(books.router, prefix="/books", tags=["Books"])

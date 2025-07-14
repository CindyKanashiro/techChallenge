from fastapi import FastAPI
from api.routes.books import router as books_router

app = FastAPI(title="Books API", version="1.0")

app.include_router(books_router)

from fastapi import FastAPI
import uvicorn
from routes import books
from routes import auth

app = FastAPI(title="Book Public API", version="1.0.0")

app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

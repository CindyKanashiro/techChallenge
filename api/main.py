from fastapi import FastAPI
import uvicorn
from routes import books, auth, scraping


app = FastAPI(title="Book Public API", version="1.0.0")

app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(scraping.router, prefix="/scraping", tags=["Scraping"])
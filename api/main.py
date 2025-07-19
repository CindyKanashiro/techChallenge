from fastapi import FastAPI
import uvicorn
from routes import auth, scraping
from routes.books import router as books_router


app = FastAPI(title="Books API", version="1.0")

app.include_router(books_router)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(scraping.router, prefix="/scraping", tags=["Scraping"])

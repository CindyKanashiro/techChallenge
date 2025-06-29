from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_books():
    return [
        {"title": "1984", "author": "George Orwell"},
        {"title": "Clean Code", "author": "Robert C. Martin"},
    ]

from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: int
    title: str
    price: float
    rating: int
    stock: int
    category: Optional[str] = None
    cover: Optional[str] = None  # Base64 encoded image data
    
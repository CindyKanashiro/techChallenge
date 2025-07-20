from sqlalchemy import Column, Integer, String, Float
from api.database import Base


class BookORM(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    price = Column(Float)
    rating = Column(Integer)
    stock = Column(Integer)
    category = Column(String)
    cover = Column(String)


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

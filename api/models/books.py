from sqlalchemy import Column, Float, Integer, LargeBinary, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    cover = Column(LargeBinary)

from pydantic import Base64Bytes, BaseModel, ConfigDict


class BookSchema(BaseModel):
    title: str
    price: float
    rating: int
    stock: int
    category: str
    cover: Base64Bytes

    model_config = ConfigDict(from_attributes=True)

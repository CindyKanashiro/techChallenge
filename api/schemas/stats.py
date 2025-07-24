from pydantic import BaseModel, ConfigDict


class RatingsDistributionSchema(BaseModel):
    rating: int
    count: int

    model_config = ConfigDict(from_attributes=True)


class BooksSummarySchema(BaseModel):
    number_of_books: int
    average_price: float
    rating_distribution: list[RatingsDistributionSchema]

    model_config = ConfigDict(from_attributes=True)


class CategoriesSummarySchema(BaseModel):
    category: str
    number_of_books: int
    average_price: float

    model_config = ConfigDict(from_attributes=True)

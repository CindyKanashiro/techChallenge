from typing import List
from pydantic import BaseModel, ConfigDict

class PredictResultSchema(BaseModel):
    category: str

    model_config = ConfigDict(from_attributes=True)

class PredictionRequest(BaseModel):
    title: str


class FeaturesResponse(BaseModel):
    features: List[List[float]]
    feature_names: List[str]

class TrainData(BaseModel):
    title: str
    category: str

    model_config = ConfigDict(from_attributes=True)
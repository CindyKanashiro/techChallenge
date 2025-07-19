from fastapi import APIRouter
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

from models import DataToPrediction


router = APIRouter()

model = joblib.load("modelo_classificacao_de_descricao.pkl")

@router.get("/features")
def format_data():
    ...

@router.get("/training-data")
def training_data():
    ...

@router.post("/predictions")
def prediction(
    pred_data: DataToPrediction
):
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    x_vec = vectorizer.fit_transform(pred_data.description)
    result = model.predict(x_vec)
    breakpoint()
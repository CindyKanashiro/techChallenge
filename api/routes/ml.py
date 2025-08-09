from fastapi import APIRouter
import joblib
from api.core.database import get_books_session
from api.models.books import BookModel
from api.schemas.books import BookSchema
from api.schemas.ml import FeaturesResponse, PredictResultSchema, PredictionRequest, TrainData

router = APIRouter(
    prefix="/api/v1/ml", 
    tags=["Machine-Learning"]
)



@router.get(
    "/features",
    response_model=FeaturesResponse,
    summary="Features",
    description="Retorna features do dataset.",
)
def get_features():
    pipeline = joblib.load('data/model_books.pkl')
    vectorizer = pipeline.named_steps['tfidf']
    X_transformed = vectorizer.transform(["Harry Potter"])

    return FeaturesResponse(
        features=X_transformed.toarray().tolist(),
        feature_names=vectorizer.get_feature_names_out().tolist()
    )


@router.get(
    "/training-data",
    response_model=list[TrainData],
    summary="Training Data",
    description="Dataset de treinamento para o modelo.",
)
def get_training_data() -> list[TrainData]:
    with get_books_session() as db:
        return list(
            map(
                TrainData.model_validate, 
                db.query(
                    BookModel
                ).with_entities(
                    BookModel.title, 
                    BookModel.category
                ).filter(
                    BookModel.category.not_in(["Default"]))))

@router.post(
    "/predictions",
    response_model=PredictResultSchema,
    summary="Prediction",
    description="Define a categoria do livro pelo titulo"
)
def predict(request: PredictionRequest):
    model = joblib.load('data/model_books.pkl')
    prediction = model.predict([request.title])
    return PredictResultSchema(category=prediction[0])

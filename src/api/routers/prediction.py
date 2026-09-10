from fastapi import APIRouter, Depends, Query

from src.api.schemas.prediction import (
    PredictionHistoryResponse,
    PredictionRequest,
    PredictionResponse,
)
from src.api.services.prediction_service import PredictionService
from src.dependencies.auth import get_current_user
from src.dependencies.database import get_db
from src.dependencies.model import get_model

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post("", status_code=200, response_model=PredictionResponse)
def predict(
    df: PredictionRequest,
    model=Depends(get_model),
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    service = PredictionService(model=model, db=db)
    return service.predict(df, user)


@router.get("/history/{id}", response_model=PredictionHistoryResponse)
def get_prediction(id: int, db=Depends(get_db), user=Depends(get_current_user)):
    service = PredictionService(db=db)

    return service.get_prediction(prediction_id=id, user=user)


@router.get("/history", response_model=list[PredictionHistoryResponse])
def get_history(
    db=Depends(get_db),
    user=Depends(get_current_user),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    condition: str | None = Query(default=None, description="Prediction type"),
):
    service = PredictionService(db=db)

    return service.get_prediction_history(
        user=user, limit=limit, offset=offset, condition=condition
    )


@router.delete("/delete/{id}")
def delete_prediction(id: int, db=Depends(get_db), user=Depends(get_current_user)):
    service = PredictionService(db=db)

    service.delete_prediction(prediction_id=id, user=user)

    return f"The prediction with id {id} was successfully removed."

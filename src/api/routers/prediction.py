from fastapi import APIRouter, Depends, HTTPException
from src.api.schemas.prediction import PredictionRequest, PredictionResponse, PredictionHistoryResponse
from src.dependencies.model import get_model
from src.dependencies.database import get_db
from src.api.services.prediction_service import PredictionService
from src.api.core.logger import logger
from src.dependencies.auth import get_current_user

router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("", status_code=200, response_model=PredictionResponse)
def predict(df:PredictionRequest, model = Depends(get_model), db= Depends(get_db), user=Depends(get_current_user)):
    try:
        service = PredictionService(model=model, db=db)
        return service.predict(df, user)
    except Exception as e:
        logger.exception(e)

        raise HTTPException(status_code=500, detail="Prediction failed.")

@router.get("/history/{id}", response_model=PredictionHistoryResponse)
def get_prediction(id: int, db = Depends(get_db), model = Depends(get_model), user= Depends(get_current_user)):
    service = PredictionService(db=db, model=model)

    return service.get_prediction(prediction_id=id, user=user)

    

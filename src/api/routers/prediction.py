from fastapi import APIRouter, Depends, HTTPException
from src.api.schemas.prediction import PredictionRequest, PredictionResponse
from src.dependencies.model import get_model
from src.dependencies.database import get_db
from src.api.services.prediction_service import PredictionService
from src.api.core.logger import logger

router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("", status_code=200, response_model=PredictionResponse)
def predict(df:PredictionRequest, model = Depends(get_model), db= Depends(get_db)):
    try:
        service = PredictionService(model=model, db=db)
        return service.predict(df)
    except Exception as e:
        logger.exception(e)

        HTTPException(status_code=500, detail="Prediction failed.")
    

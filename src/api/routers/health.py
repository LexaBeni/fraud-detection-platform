from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.dependencies.database import get_db
from src.dependencies.model import get_model

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
def health_check(db: Session = Depends(get_db), model = Depends(get_model)):
    model_status = model is not None

    try:
        db.execute(text("SELECT 1"))
        database_status = True
    except Exception:
        database_status = False

    is_healthy = model_status and database_status

    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "model": "ok" if model_status else "unavailable",
        "database": "ok" if database_status else "unavailable",
    }
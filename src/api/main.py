from fastapi import FastAPI
from src.api.routers.health import router as health_router
from src.api.routers.prediction import router as prediction_router
from contextlib import asynccontextmanager
from src.api.core.logger import logger
from src.api.core.settings import settings
import joblib
from src.api.core.database import Base, engine, SessionLocal
from src.api.models.prediction import Prediction
import time
from src.api.services.bootstrap_service import ensure_admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading model...")
    try:
        app.state.model = joblib.load(settings.model_path)
    except Exception as e:
        logger.exception("Model loading failed")
        raise RuntimeError("Model loading failed")

    with SessionLocal() as db:
        ensure_admin(db)
        
    yield

    logger.info("Server is shutting down...")

app = FastAPI(title="Fraud Detection API", version="1.0.0", lifespan=lifespan)

@app.middleware("http")
async def middleware(request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start_time

    response.headers["X-Process-Time"] = str(duration)

    logger.info(f"{request.method} {request.url.path} completed in {duration:.4f} seconds")

    return response

app.include_router(health_router)
app.include_router(prediction_router)
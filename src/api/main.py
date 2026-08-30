from fastapi import FastAPI
from src.api.routers.health import router as health_router
from contextlib import asynccontextmanager
from src.api.core.logger import logger
from src.api.core.settings import settings
import joblib
from src.api.core.database import Base, engine
from src.api.models.prediction import Prediction
import time

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading model...")
    try:
        app.state.model = joblib.load(settings.model_path)
    except Exception as e:
        logger.exception("Model loading failed")
        raise RuntimeError("Model loading failed")

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
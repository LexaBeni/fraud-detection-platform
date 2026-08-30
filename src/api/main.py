from fastapi import FastAPI
from src.api.routers.health import router as health_router

app = FastAPI(title="Fraud Detection API", version="1.0.0")

app.include_router(health_router)
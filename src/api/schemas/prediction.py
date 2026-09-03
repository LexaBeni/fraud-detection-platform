from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PredictionRequest(BaseModel):
    TransactionDT: int
    TransactionAmt: float
    ProductCD: str
    P_emaildomain: Optional[str] = None
    R_emaildomain: Optional[str] = None
    card1: Optional[int] = None
    card2: Optional[int] = None
    card4: Optional[str] = None
    card5: Optional[int] = None
    card6: Optional[str] = None
    addr1: Optional[int] = None
    addr2: Optional[int] = None
    dist1: Optional[float] = None
    dist2: Optional[float] = None
    D1: float | None = None

class PredictionResponse(BaseModel):
    prediction: str
    probability: float

class PredictionHistoryResponse(BaseModel):
    prediction: str
    probability: float
    threshold: float
    created_at: datetime
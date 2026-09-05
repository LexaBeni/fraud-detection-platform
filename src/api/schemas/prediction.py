from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime

class PredictionRequest(BaseModel):
    TransactionDT: int = Field(ge=0, description="Timedelta from a given reference datetime")
    TransactionAmt: float = Field(ge=0, description="Transaction payment amount in USD")
    ProductCD: str = Field(description="Product code, the product for each transaction")
    P_emaildomain: Optional[str] = Field(None, description="Purchaser email domain")
    R_emaildomain: Optional[str] = Field(None, description="Recipient email domain")
    card1: Optional[int] = Field(None, description="Payment card information (e.g., card series)", ge=1000)
    card2: Optional[int] = Field(None, description="Payment card information (e.g., bank ID)", ge=100)
    card4: Optional[str] = Field(None, description="Card type (e.g., visa, mastercard, discover, amex)")
    card5: Optional[int] = Field(None, description="Payment card information (e.g., bank category)", ge=100)
    card6: Optional[str] = Field(None, description="Card category (e.g., credit, debit)")
    addr1: Optional[int] = Field(None, description="Billing region/zip code")
    addr2: Optional[int] = Field(None, description="Billing country code")
    dist1: Optional[float] = Field(None, description="Distance between billing address and zip code", ge=0)
    dist2: Optional[float] = Field(None, description="Distance from alternative address", ge=0)
    D1: Optional[float] = Field(None, description="Timedelta, such as days since last transaction", ge=0)

    @field_validator("ProductCD")
    @classmethod
    def validate_product(cls, v):
        allowed = {'W', 'H', 'C', 'S', 'R'}
        if v not in allowed:
            raise ValueError(f"ProductCD must be one of {allowed}")
        return v

    @field_validator("card4")
    @classmethod
    def validate_card4(cls, v):
        if not v:
            return v
        allowed = {'visa', 'mastercard', 'american express', 'discover'}

        if v.lower() not in allowed:
             raise ValueError(f"card4 must be one of {allowed}")
        return v.lower()

    @field_validator("card6")
    @classmethod
    def validate_card6(cls, v):
        if not v:
            return v
        allowed = ('credit', 'debit', 'debit or credit', 'charge card')

        if v.lower() not in allowed:
            raise ValueError(f"card6 must be one of {allowed}")
        return v.lower()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "TransactionDT": 86400,
                "TransactionAmt": 49.50,
                "ProductCD": "W",
                "P_emaildomain": "gmail.com",
                "R_emaildomain": None,
                "card1": 13926,
                "card2": 327,
                "card4": "discover",
                "card5": 162,
                "card6": "credit",
                "addr1": 315,
                "addr2": 87,
                "dist1": 19.0,
                "dist2": None,
                "D1": 14.0
            }
        }
    )
    
class PredictionResponse(BaseModel):
    prediction: str
    probability: float

class PredictionHistoryResponse(BaseModel):
    prediction: str
    probability: float
    threshold: float
    created_at: datetime
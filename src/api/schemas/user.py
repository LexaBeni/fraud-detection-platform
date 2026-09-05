from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr = Field(min_length=5, max_length=75, description="User email")
    password: str = Field(min_length=3, max_length=50, description="User password")

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    role: str
    created_at: datetime
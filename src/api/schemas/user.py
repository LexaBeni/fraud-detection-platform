from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    email: EmailStr = Field(min_length=5, max_length=75, description="User email")
    password: str = Field(min_length=3, max_length=50, description="User password")
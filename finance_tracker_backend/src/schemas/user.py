from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Input schema for creating a user."""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="Plain user password")


class UserRead(BaseModel):
    """Output schema for reading user information."""
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.models.transaction import TransactionType


class TransactionCreate(BaseModel):
    """Schema for creating a transaction."""
    amount: float = Field(..., gt=0)
    type: TransactionType = Field(..., description="income or expense")
    category: str = Field(..., min_length=1, max_length=100)
    date: datetime = Field(default_factory=datetime.utcnow)
    note: Optional[str] = Field(default=None, max_length=1000)


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction."""
    amount: Optional[float] = Field(default=None, gt=0)
    type: Optional[TransactionType] = Field(default=None)
    category: Optional[str] = Field(default=None, min_length=1, max_length=100)
    date: Optional[datetime] = Field(default=None)
    note: Optional[str] = Field(default=None, max_length=1000)


class TransactionRead(BaseModel):
    """Schema for reading a transaction."""
    id: int
    user_id: int
    amount: float
    type: TransactionType
    category: str
    date: datetime
    note: Optional[str] = None

    class Config:
        from_attributes = True


class TransactionListFilters(BaseModel):
    """Filters for listing transactions."""
    start_date: Optional[datetime] = Field(default=None, description="Start datetime inclusive")
    end_date: Optional[datetime] = Field(default=None, description="End datetime inclusive")
    type: Optional[TransactionType] = Field(default=None)
    category: Optional[str] = Field(default=None)

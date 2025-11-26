from datetime import datetime

from pydantic import BaseModel, Field


class Summary(BaseModel):
    """High-level budget summary."""
    total_income: float = Field(..., description="Total income for period")
    total_expense: float = Field(..., description="Total expense for period")
    balance: float = Field(..., description="Income - Expense for period")


class ByCategoryItem(BaseModel):
    """Aggregated amount by a category."""
    category: str = Field(..., description="Category name")
    amount: float = Field(..., description="Total amount for this category")
    type: str = Field(..., description="income or expense")


class TrendPoint(BaseModel):
    """Amount aggregated per time bucket for charting trends."""
    period_start: datetime = Field(..., description="Start of period (e.g., week/month)")
    income: float = Field(..., description="Income sum")
    expense: float = Field(..., description="Expense sum")

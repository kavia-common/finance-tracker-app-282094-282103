from typing import Generic, Sequence, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Parameters for pagination and common listing use-cases."""
    page: int = Field(default=1, ge=1, description="Page number starting from 1")
    per_page: int = Field(default=20, ge=1, le=200, description="Items per page, max 200")


class Paginated(GenericModel, Generic[T]):
    """A generic paginated response wrapper."""
    items: Sequence[T] = Field(default_factory=list, description="List of items on this page")
    total: int = Field(..., description="Total number of items matching the filter")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")

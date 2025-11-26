from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Schema for login credentials."""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="User password")


class RegisterRequest(BaseModel):
    """Schema for registration request."""
    name: str = Field(..., min_length=1, max_length=255, description="Full name")
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="User password")


class Token(BaseModel):
    """Schema for JWT access token response."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")

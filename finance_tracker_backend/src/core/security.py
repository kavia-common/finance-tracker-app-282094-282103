from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.core.config import get_settings
from src.core.db import get_db
from src.models.user import User
from src.repositories.user_repo import get_by_email

settings = get_settings()

# OAuth2 scheme definition for "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# PUBLIC_INTERFACE
def create_access_token(subject: str, expires_delta_minutes: Optional[int] = None) -> str:
    """Create a signed JWT access token with subject (e.g., user email)."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_delta_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    return encoded_jwt


def _decode_token(token: str) -> Optional[str]:
    """Decode a JWT and return the subject (email) if valid, else None."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        return payload.get("sub")
    except JWTError:
        return None


# PUBLIC_INTERFACE
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """FastAPI dependency to resolve the currently authenticated user from a JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    subject = _decode_token(token)
    if subject is None:
        raise credentials_exception

    user = get_by_email(db, subject)
    if not user:
        raise credentials_exception
    return user

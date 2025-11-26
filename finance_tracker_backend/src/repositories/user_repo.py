from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verify a plain password against a password hash."""
    return pwd_context.verify(plain_password, password_hash)


# PUBLIC_INTERFACE
def get_by_email(db: Session, email: str) -> Optional[User]:
    """Return a user by email if exists, else None."""
    return db.query(User).filter(User.email == email).first()


# PUBLIC_INTERFACE
def create(db: Session, name: str, email: str, password: str) -> User:
    """Create a new user with hashed password."""
    user = User(name=name, email=email, password_hash=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

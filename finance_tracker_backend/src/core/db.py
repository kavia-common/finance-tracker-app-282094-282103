from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from src.core.config import get_settings

settings = get_settings()

# Sqlite requires check_same_thread=False when used with multiple threads like FastAPI/uvicorn
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
    pool_pre_ping=True,
)

# SessionLocal factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session and ensures proper close."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# PUBLIC_INTERFACE
def init_db() -> None:
    """Initialize database tables using SQLAlchemy metadata create_all."""
    # Import models to ensure they are registered with Base.metadata before create_all
    from src.models import user, transaction  # noqa: F401

    Base.metadata.create_all(bind=engine)


@contextmanager
def db_session() -> Generator[Session, None, None]:
    """Context manager for manual session management in scripts or services."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

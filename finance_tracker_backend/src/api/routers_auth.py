from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.core.security import create_access_token, get_current_user
from src.models.user import User
from src.repositories.user_repo import create as create_user, get_by_email, verify_password
from src.schemas.auth import LoginRequest, RegisterRequest, Token
from src.schemas.user import UserRead

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserRead,
    summary="Register a new user",
    description="Create a new user account with name, email, and password.",
    status_code=status.HTTP_201_CREATED,
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> UserRead:
    existing = get_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, name=payload.name, email=payload.email, password=payload.password)
    return UserRead.model_validate(user)


@router.post(
    "/login",
    response_model=Token,
    summary="Login and get access token",
    description="Authenticate using email and password and receive a JWT access token.",
)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> Token:
    user = get_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(subject=user.email)
    return Token(access_token=token, token_type="bearer")


@router.post(
    "/token",
    response_model=Token,
    summary="OAuth2 token endpoint",
    description="OAuth2PasswordBearer-compatible token endpoint accepting form-encoded credentials.",
)
def oauth_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    user = get_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(subject=user.email)
    return Token(access_token=token, token_type="bearer")


@router.get(
    "/me",
    response_model=UserRead,
    summary="Get current user",
    description="Return the profile of the current authenticated user.",
)
def me(current_user: User = Depends(get_current_user)) -> UserRead:
    return UserRead.model_validate(current_user)

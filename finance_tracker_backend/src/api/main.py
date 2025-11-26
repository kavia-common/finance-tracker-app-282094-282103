from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.db import init_db
from src.core.config import get_settings
from src.api.routers_auth import router as auth_router
from src.api.routers_transactions import router as transactions_router
from src.api.routers_budget import router as budget_router

# Initialize FastAPI app with basic metadata
app = FastAPI(
    title="Finance Tracker API",
    description="Backend API for authentication, transactions, and budgeting analytics.",
    version="0.1.0",
    openapi_tags=[
        {"name": "Health", "description": "Service health and diagnostics"},
        {"name": "Auth", "description": "User registration and authentication"},
        {"name": "Transactions", "description": "CRUD operations for transactions"},
        {"name": "Budget", "description": "Budget analytics and summaries"},
    ],
)

# Load settings for CORS configuration
_settings = get_settings()
cors_origins_raw = _settings.CORS_ALLOW_ORIGINS or "*"
allow_origins = (
    ["*"]
    if cors_origins_raw.strip() == "*"
    else [o.strip() for o in cors_origins_raw.split(",") if o.strip()]
)

# CORS settings from env (default '*')
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Initialize database tables on application startup."""
    init_db()


@app.get("/", summary="Health Check", tags=["Health"])
def health_check():
    """Health check endpoint to verify the API is running."""
    return {"message": "Healthy"}


# Include routers
app.include_router(auth_router)
app.include_router(transactions_router)
app.include_router(budget_router)

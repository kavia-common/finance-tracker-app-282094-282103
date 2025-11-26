from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.db import init_db

# Initialize FastAPI app with basic metadata
app = FastAPI(
    title="Finance Tracker API",
    description="Backend API for authentication, transactions, and budgeting analytics.",
    version="0.1.0",
)

# CORS settings - permissive for now, can be tightened later via env
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

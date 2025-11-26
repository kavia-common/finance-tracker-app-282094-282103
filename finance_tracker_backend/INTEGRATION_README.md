# Finance Tracker Integration Notes

This document summarizes how the backend and frontend integrate and how to configure environments.

## Backend (FastAPI)

- Configuration is loaded from environment variables via `src/core/config.py` (using `python-dotenv`).
- Defaults:
  - DATABASE_URL: `sqlite:///./data.db`
  - JWT_SECRET: `change-me`
  - JWT_ALG: `HS256`
  - ACCESS_TOKEN_EXPIRE_MINUTES: `60`
  - CORS_ALLOW_ORIGINS: `*` (use a CSV list for specific origins)

Create a `.env` file based on `.env.example` to override defaults.

### CORS
CORS is configured from `CORS_ALLOW_ORIGINS`. Use:
- `*` for all origins (development)
- `http://localhost:3000,http://localhost:8080` for specific origins (recommended for deployed environments)

### OpenAPI generation
The backend includes a helper to dump the current OpenAPI schema:

```
# from repository root:
cd finance-tracker-app-282094-282103/finance_tracker_backend
python -m src.api.generate_openapi
```

The schema is saved to `interfaces/openapi.json`. Commit this file so the frontend (and other consumers) can align models.

## Frontend (Flutter)

- The frontend must read API base URL from an environment variable and pass Bearer tokens from the login response.
- Ensure an `.env` file with `API_BASE_URL` is present in the frontend root.
- The frontend models should align with the backend OpenAPI in `interfaces/openapi.json`:
  - Auth: `Token` with `access_token` and `token_type` (default `bearer`)
  - Transactions: see `TransactionCreate`, `TransactionRead`, `TransactionUpdate`
  - Budget: `Summary`, `ByCategoryItem`, `TrendPoint`

### Typical environment
```
API_BASE_URL=http://localhost:3001
```

If the backend is served on a different host or path, set accordingly, e.g.:
```
API_BASE_URL=https://api.mycompany.com
```

## Run locally

- Backend:
  - Copy `.env.example` to `.env`, customize as needed.
  - Run: `uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload`

- Frontend:
  - Ensure `.env` exists with `API_BASE_URL`.
  - Run the Flutter app on the emulator/device.

## Security note

Change `JWT_SECRET` and restrict `CORS_ALLOW_ORIGINS` for non-development environments.

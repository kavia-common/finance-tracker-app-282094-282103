# Finance Tracker - Final Integration Guide

This guide summarizes how to connect the Flutter frontend with the FastAPI backend.

## 1) Backend configuration

- Copy `finance_tracker_backend/.env.example` to `finance_tracker_backend/.env` and adjust values.
- Defaults:
  - SQLite database: `sqlite:///./data.db`
  - JWT settings: `JWT_SECRET=change-me`, `JWT_ALG=HS256`, `ACCESS_TOKEN_EXPIRE_MINUTES=60`
  - CORS: `CORS_ALLOW_ORIGINS=*` (adjust for deployed domains)

Run backend locally:
```
cd finance-tracker-app-282094-282103/finance_tracker_backend
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
```

## 2) Frontend configuration

- Copy `finance-tracker-app-282094-282104/finance_tracker_frontend/.env.example` to `.env` in the same folder and set:
```
API_BASE_URL=http://localhost:3001
```
Android emulator host mapping uses `10.0.2.2`:
```
API_BASE_URL=http://10.0.2.2:3001
```

## 3) OpenAPI and model alignment

Regenerate backend OpenAPI when routes/models change:
```
cd finance-tracker-app-282094-282103/finance_tracker_backend
python -m src.api.generate_openapi
```
The spec is written to `interfaces/openapi.json`. Ensure frontend models adhere to:
- Token (access_token, token_type)
- TransactionCreate/Read/Update
- Summary, ByCategoryItem, TrendPoint
- Pagination wrapper `Paginated[TransactionRead]` for listing

## 4) Auth and headers

- Login via `POST /auth/login` using body `{ "email": "...", "password": "..." }`
- Use returned `access_token` as `Authorization: Bearer <token>` for protected endpoints.

## 5) CORS

CORS origins are controlled by `CORS_ALLOW_ORIGINS` in backend `.env`. Use a CSV list in production (no spaces), or `*` during development.

Security: Use a strong `JWT_SECRET` and restrict CORS in production.

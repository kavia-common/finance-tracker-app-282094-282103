# finance-tracker-app-282094-282103

This monorepo contains:
- finance_tracker_backend (FastAPI)
- finance_tracker_frontend (Flutter) in sibling workspace `finance-tracker-app-282094-282104/finance_tracker_frontend`

## Final Integration Checklist

Backend:
- Config reads from `.env` with sensible defaults (SQLite, JWT settings)
- CORS configured via `CORS_ALLOW_ORIGINS`
- OpenAPI spec generated at `finance_tracker_backend/interfaces/openapi.json` using:
  ```
  cd finance-tracker-app-282094-282103/finance_tracker_backend
  python -m src.api.generate_openapi
  ```

Frontend:
- Uses `API_BASE_URL` from `.env` to build API client
- Aligns models with backend spec (Auth, Transactions, Budget)

See `finance_tracker_backend/INTEGRATION_README.md` and frontend `INTEGRATION_README.md` for details.
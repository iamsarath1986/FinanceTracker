# FinanceTracker

Personal single-user finance tracker. Manages income, expenses, and deposit accounts across multiple banks and currencies.

## Stack

**Backend:** FastAPI + SQLAlchemy + Alembic + PostgreSQL (Docker) / SQLite (dev)
**Frontend:** Vue 3 + TypeScript + Vite + PrimeVue + Pinia
**Auth:** PIN from `.env` (`APP_PIN`), JWT HS256 24h token. No user model — all routes protected by `get_current_session` dep.

## Project Structure

```
backend/app/
  api/          # Route handlers (auth, accounts, categories, transactions, recurring, budgets, dashboard)
  core/         # config.py (pydantic-settings), security.py (PIN verify, JWT), limiter.py
  db/           # session.py — SQLAlchemy engine + SessionLocal + Base
  models/       # SQLAlchemy ORM models
  schemas/      # Pydantic request/response schemas
  services/     # dashboard.py (summary queries), recurring.py (generate_due)

frontend/src/
  api/          # Axios client + per-resource modules
  stores/       # Pinia stores (auth.ts)
  pages/        # Route-level Vue pages
  components/   # Shared components (layout/, dashboard/)
  types/        # TypeScript interfaces mirroring backend schemas
```

## Key Architecture Rules

**Account balance** is computed dynamically: `opening_balance + SUM(income) - SUM(expenses)`. Never store as a field.

**Budgets** support 4 combinations: `scope_type (category|account)` × `period_type (monthly|annual)`. `month` is nullable (null = annual). `spent` is computed at query time.

**Recurring transactions** are Phase 1. `services/recurring.generate_due()` creates Transaction rows for all dates from `last_generated_date` to today. Called on dashboard load and transaction list load.

**Currency** — each account stores its own ISO 4217 currency. No conversion logic until Phase 2.

**CORS** — `EnsureCorsOnErrors` middleware in `main.py` guarantees headers reach the browser even on 401/500 responses that bypass `CORSMiddleware`.

## Running

```bash
# Backend (Docker)
docker compose up

# Backend (local dev)
cd backend && uvicorn app.main:app --reload

# DB migrations
cd backend && alembic upgrade head

# Frontend
cd frontend && npm install && npm run dev
```

Backend: `http://localhost:8001` (Docker) or `http://localhost:8000` (local)
Frontend: `http://localhost:5173`

## Out of Scope (Phase 2)

- Account-to-account transfers
- Live exchange-rate conversion

# FinanceTracker Vue + FastAPI Project Plan

## Summary

Build FinanceTracker as a full-stack personal finance MVP with a Vue 3 + Vite + TypeScript frontend and a FastAPI backend. The first implementation should create a clean project scaffold, JWT authentication, CRUD flows for accounts/categories/transactions/budgets, and dashboard summaries. CSV import/export and richer reports can follow after the core data model is stable.

Assume the current root `main.py` is only a PyCharm placeholder and should be replaced by the planned `backend/` application structure.

## Key Changes

- Create a `backend/` FastAPI app with:
  - `app/main.py` FastAPI entrypoint
  - `app/api/` route modules
  - `app/core/` settings, security, JWT config
  - `app/db/` session and database setup
  - `app/models/` SQLAlchemy ORM models
  - `app/schemas/` Pydantic request/response schemas
  - `app/services/` business logic
  - `app/tests/` pytest tests
  - `alembic/` migrations

- Create a `frontend/` Vue app with:
  - Vue 3, Vite, TypeScript
  - Vue Router for pages
  - Pinia for auth/session and app state
  - Axios API client
  - Page structure for login, register, dashboard, accounts, categories, transactions, budgets, and reports

- Use SQLite for local development by default and keep configuration compatible with PostgreSQL for production.

## Backend Plan

- Dependencies:
  - `fastapi`, `uvicorn`
  - `sqlalchemy`, `alembic`
  - `pydantic-settings`
  - `python-jose` or `pyjwt` for JWT
  - `passlib[bcrypt]` for password hashing
  - `pytest`, `httpx`

- Core entities:
  - `User`: email, hashed password, timestamps
  - `Account`: user-owned account name, type, currency, opening/current balance
  - `Category`: user-owned category name, type `income` or `expense`
  - `Transaction`: account, optional category, amount, type, date, description
  - `Budget`: category, period/month, limit amount
  - Dashboard summary derived from transactions and budgets

- API routes:
  - `POST /auth/register`
  - `POST /auth/login`
  - `GET /auth/me`
  - CRUD routes for `/accounts`, `/categories`, `/transactions`, `/budgets`
  - `GET /dashboard/summary`
  - Later: `/reports`, `/import`, `/export`

- Behavior:
  - All finance data is scoped to the authenticated user.
  - JWT bearer token protects private endpoints.
  - Server validates ownership before reading, updating, or deleting records.
  - Transactions update dashboard summaries through queries, not duplicated stored totals for MVP.

## Frontend Plan

- Pages:
  - `LoginPage`
  - `RegisterPage`
  - `DashboardPage`
  - `AccountsPage`
  - `CategoriesPage`
  - `TransactionsPage`
  - `BudgetsPage`
  - `ReportsPage`

- Layout:
  - Auth pages use a minimal centered form.
  - App pages use a persistent sidebar/top navigation.
  - Dashboard shows account balances, income, expenses, net cash flow, budget progress, and recent transactions.

- State and API:
  - Pinia `authStore` stores token and current user.
  - Axios instance injects `Authorization: Bearer <token>`.
  - Route guards redirect unauthenticated users to login.
  - Each feature page calls backend CRUD APIs directly through typed frontend API modules.

## Implementation Order

1. Scaffold backend and frontend directories.
2. Add backend settings, database connection, Alembic setup, and health route.
3. Add user model, auth schemas, password hashing, JWT login/register.
4. Add protected route dependency and `/auth/me`.
5. Implement account and category CRUD.
6. Implement transaction CRUD.
7. Implement budget CRUD.
8. Implement dashboard summary endpoint.
9. Scaffold Vue app with router, Pinia, API client, and auth flow.
10. Build dashboard and CRUD pages.
11. Add backend tests for auth and core CRUD flows.
12. Update `README.md` with exact setup commands.

## Test Plan

- Backend pytest coverage:
  - User registration succeeds with valid data.
  - Duplicate email registration fails.
  - Login returns JWT for valid credentials.
  - Protected endpoints reject missing/invalid token.
  - Users cannot access another user's accounts, categories, transactions, or budgets.
  - CRUD flows work for accounts, categories, transactions, and budgets.
  - Dashboard summary returns correct income, expense, balance, and budget values.

- Frontend checks:
  - App builds with `npm run build`.
  - Login/register flows store auth token.
  - Protected routes redirect when logged out.
  - CRUD pages render loading, empty, success, and error states.

## Assumptions

- MVP uses SQLite locally and PostgreSQL-ready SQLAlchemy models.
- Backend uses SQLAlchemy rather than SQLModel.
- Frontend uses Pinia for state management.
- CSV import/export and advanced charts are phase-two features after the core MVP.
- The root `main.py` can be removed or ignored once `backend/app/main.py` exists.

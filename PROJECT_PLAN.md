# FinanceTracker — Full Implementation Plan

## Context

Personal finance tracker for a single user managing income, expenses, and deposit accounts (savings, investments) across multiple banks in different countries. Accounts may hold different currencies. The app needs budgets at multiple scopes (monthly/annual × category/account), recurring transactions, and a dashboard summary. No multi-user support — auth is a simple PIN stored in `.env`. Frontend is Vue 3 + TypeScript + Vite + PrimeVue. Backend is FastAPI + SQLAlchemy + SQLite (dev).

**Phase 2 (out of scope here):** account-to-account transfers, live exchange-rate conversions.

---

## Project Structure

```
FinanceTracker/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── accounts.py
│   │   │   ├── categories.py
│   │   │   ├── transactions.py
│   │   │   ├── recurring.py
│   │   │   ├── budgets.py
│   │   │   └── dashboard.py
│   │   ├── core/
│   │   │   ├── config.py        # pydantic-settings: APP_PIN, DATABASE_URL, SECRET_KEY
│   │   │   └── security.py      # PIN verify, JWT create/decode, get_current_session dep
│   │   ├── db/
│   │   │   └── session.py       # SQLAlchemy engine + SessionLocal + Base
│   │   ├── models/
│   │   │   ├── account.py
│   │   │   ├── category.py
│   │   │   ├── transaction.py
│   │   │   ├── recurring.py
│   │   │   └── budget.py
│   │   ├── schemas/
│   │   │   ├── account.py
│   │   │   ├── category.py
│   │   │   ├── transaction.py
│   │   │   ├── recurring.py
│   │   │   ├── budget.py
│   │   │   └── dashboard.py
│   │   ├── services/
│   │   │   ├── dashboard.py     # summary query logic
│   │   │   └── recurring.py     # generate due transactions
│   │   └── tests/
│   │       ├── conftest.py
│   │       ├── test_auth.py
│   │       ├── test_accounts.py
│   │       ├── test_transactions.py
│   │       └── test_budgets.py
│   ├── alembic/
│   ├── alembic.ini
│   ├── requirements.txt
│   └── .env                     # APP_PIN, SECRET_KEY, DATABASE_URL
├── frontend/
│   ├── src/
│   │   ├── main.ts
│   │   ├── App.vue
│   │   ├── router/index.ts
│   │   ├── stores/
│   │   │   └── auth.ts          # Pinia: token, isAuthenticated, login(), logout()
│   │   ├── api/
│   │   │   ├── client.ts        # Axios instance with Bearer token interceptor
│   │   │   ├── accounts.ts
│   │   │   ├── categories.ts
│   │   │   ├── transactions.ts
│   │   │   ├── recurring.ts
│   │   │   ├── budgets.ts
│   │   │   └── dashboard.ts
│   │   ├── pages/
│   │   │   ├── LoginPage.vue
│   │   │   ├── DashboardPage.vue
│   │   │   ├── AccountsPage.vue
│   │   │   ├── CategoriesPage.vue
│   │   │   ├── TransactionsPage.vue
│   │   │   ├── RecurringPage.vue
│   │   │   ├── BudgetsPage.vue
│   │   │   └── ReportsPage.vue
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── AppSidebar.vue
│   │   │   │   └── AppTopbar.vue
│   │   │   └── dashboard/
│   │   │       ├── BalanceCard.vue
│   │   │       ├── CashFlowChart.vue   # PrimeVue Chart.js wrapper
│   │   │       └── BudgetProgress.vue
│   │   └── types/index.ts       # TypeScript interfaces mirroring backend schemas
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
└── README.md
```

---

## Data Models

### Account
```
id, name, type (savings|investments|checking|credit_card|cash),
bank_name, country (ISO 3166), currency (ISO 4217),
opening_balance (Decimal), created_at, updated_at

current_balance is computed: opening_balance + SUM(income) - SUM(expenses)
```

### Category
```
id, name, type (income|expense), color (hex), icon
Default categories seeded on first run.
```

### Transaction
```
id, account_id (FK), category_id (FK nullable),
amount (Decimal, always positive), type (income|expense),
date, description, is_recurring (bool), recurring_id (FK nullable),
created_at
```

### RecurringTransaction
```
id, account_id (FK), category_id (FK nullable),
amount (Decimal), type (income|expense), description,
frequency (daily|weekly|monthly|yearly),
start_date, end_date (nullable), last_generated_date (nullable),
is_active (bool)
```

### Budget
```
id, name,
scope_type (category|account),
period_type (monthly|annual),
category_id (FK nullable),   -- set when scope_type = category
account_id (FK nullable),    -- set when scope_type = account
year (int), month (int nullable),  -- month=null for annual budgets
limit_amount (Decimal), currency (display only)

spent is computed at query time from transactions
```

---

## Auth (Simple PIN)

- `APP_PIN` stored in `.env`
- `POST /auth/login` body `{ "pin": "..." }` → verifies against `APP_PIN`, returns `{ "access_token": "...", "token_type": "bearer" }`
- Token is a plain JWT (HS256) signed with `SECRET_KEY`, 24h expiry, no user claim
- `get_current_session` FastAPI dependency decodes + validates token on all protected routes
- Frontend stores token in `localStorage`; Pinia `authStore` exposes `isAuthenticated`
- Vue Router guard redirects to `/login` if no valid token

---

## API Routes

```
POST   /auth/login

GET    /accounts              GET    /accounts/{id}
POST   /accounts              PUT    /accounts/{id}
DELETE /accounts/{id}

GET    /categories            GET    /categories/{id}
POST   /categories            PUT    /categories/{id}
DELETE /categories/{id}

GET    /transactions          GET    /transactions/{id}
POST   /transactions          PUT    /transactions/{id}
DELETE /transactions/{id}
# GET /transactions supports filters: account_id, category_id, type, date_from, date_to

GET    /recurring             GET    /recurring/{id}
POST   /recurring             PUT    /recurring/{id}
DELETE /recurring/{id}
POST   /recurring/{id}/generate   # manually trigger generation

GET    /budgets               GET    /budgets/{id}
POST   /budgets               PUT    /budgets/{id}
DELETE /budgets/{id}
GET    /budgets/{id}/progress     # limit vs spent

GET    /dashboard/summary
```

---

## Dashboard Summary Response

```json
{
  "accounts": [{ "id", "name", "currency", "current_balance" }],
  "monthly_cashflow": [{ "month": "2026-05", "income": 3000, "expense": 1200 }],
  "budget_progress": [{ "budget_id", "name", "limit", "spent", "currency" }],
  "recent_transactions": [ "...last 10..." ]
}
```

`current_balance` = `opening_balance + SUM(income transactions) - SUM(expense transactions)`

---

## Recurring Transaction Logic

`services/recurring.py` → `generate_due(db, recurring_id)`:
1. Load the `RecurringTransaction`
2. Compute next dates from `last_generated_date` (or `start_date`) up to `today`
3. Insert a `Transaction` for each due date
4. Update `last_generated_date`

Called automatically from `GET /transactions` and `GET /dashboard/summary` so data is always current.

---

## Implementation Order

1. **Backend scaffold** — directory structure, `requirements.txt`, `.env`, `config.py`, `session.py`, Alembic init, `GET /health`
2. **Auth** — `security.py` PIN verify + JWT, `POST /auth/login`, `get_current_session` dependency
3. **Account CRUD** — model, schema, router, Alembic migration
4. **Category CRUD** — model, schema, router, seed defaults
5. **Transaction CRUD** — model, schema, router (with filters)
6. **Recurring transactions** — model, schema, generation service, router
7. **Budget CRUD** — model, schema, router + progress endpoint
8. **Dashboard summary** — `services/dashboard.py`, `GET /dashboard/summary`
9. **Backend tests** — conftest with test DB, tests for auth/accounts/transactions/budgets
10. **Frontend scaffold** — Vite + Vue 3 + TypeScript + PrimeVue, router, Pinia, Axios client
11. **Auth store + Login page** — PIN input, token storage, route guard
12. **App layout** — `AppSidebar`, `AppTopbar`, authenticated shell
13. **Dashboard page** — balance cards, cashflow chart, budget progress bars, recent transactions table
14. **Accounts page** — DataTable, create/edit dialog, balance display
15. **Categories page** — list with color/icon, create/edit
16. **Transactions page** — DataTable with filters (account, category, type, date range), create/edit dialog
17. **Recurring page** — list with frequency/status, create/edit, manual generate button
18. **Budgets page** — list by scope/period, progress bars, create/edit dialog
19. **README** — setup commands for both backend and frontend

---

## Dependencies

### Backend (`requirements.txt`)
```
fastapi
uvicorn[standard]
sqlalchemy
alembic
pydantic-settings
python-jose[cryptography]
passlib[bcrypt]
pytest
httpx
```

### Frontend (`package.json`)
```
vue, vue-router, pinia
primevue, primeicons, @primevue/themes
axios
chart.js  (via PrimeVue's Chart component)
typescript, vite, @vitejs/plugin-vue
```

---

## Verification

- **Backend:** `cd backend && uvicorn app.main:app --reload` → `http://localhost:8000/docs`
- **Tests:** `cd backend && pytest app/tests/ -v`
- **Frontend:** `cd frontend && npm run dev` → `http://localhost:5173`

### End-to-end checks
- Login with correct PIN succeeds; wrong PIN is rejected
- Create an account (e.g. "Savings DE", EUR) — balance starts at `opening_balance`
- Add income + expense transactions — dashboard balance updates correctly
- Create a recurring monthly income — call `/generate` or wait for auto-generation — transaction appears
- Create monthly + annual category and account budgets — progress endpoint reflects spending
- Dashboard summary returns correct data for all accounts
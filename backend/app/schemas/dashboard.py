from pydantic import BaseModel

from app.schemas.transaction import TransactionOut


class AccountSummary(BaseModel):
    id: int
    name: str
    currency: str
    current_balance: float


class MonthlyCashflow(BaseModel):
    month: str
    income: float
    expense: float


class BudgetProgress(BaseModel):
    budget_id: int
    name: str
    limit_amount: float
    spent: float
    currency: str


class DashboardSummary(BaseModel):
    accounts: list[AccountSummary]
    monthly_cashflow: list[MonthlyCashflow]
    budget_progress: list[BudgetProgress]
    recent_transactions: list[TransactionOut]

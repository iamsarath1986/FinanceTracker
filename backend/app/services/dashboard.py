from decimal import Decimal

from sqlalchemy import case, extract, func
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.budget import Budget
from app.models.transaction import Transaction, TransactionType
from app.schemas.dashboard import (
    AccountSummary,
    BudgetProgress,
    DashboardSummary,
    MonthlyCashflow,
)
from app.schemas.transaction import TransactionOut


def get_account_balance(db: Session, account: Account) -> float:
    income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.account_id == account.id,
        Transaction.type == TransactionType.income,
    ).scalar() or Decimal(0)
    expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.account_id == account.id,
        Transaction.type == TransactionType.expense,
    ).scalar() or Decimal(0)
    return float(account.opening_balance + income - expense)


def get_all_account_balances(db: Session, accounts: list[Account]) -> dict[int, float]:
    if not accounts:
        return {}
    account_ids = [a.id for a in accounts]
    rows = db.query(
        Transaction.account_id,
        func.sum(case((Transaction.type == TransactionType.income, Transaction.amount), else_=0)).label("income"),
        func.sum(case((Transaction.type == TransactionType.expense, Transaction.amount), else_=0)).label("expense"),
    ).filter(Transaction.account_id.in_(account_ids)).group_by(Transaction.account_id).all()

    sums: dict[int, tuple] = {
        r.account_id: (r.income or Decimal(0), r.expense or Decimal(0))
        for r in rows
    }
    return {
        a.id: float(a.opening_balance + sums.get(a.id, (Decimal(0), Decimal(0)))[0] - sums.get(a.id, (Decimal(0), Decimal(0)))[1])
        for a in accounts
    }


def get_budget_spent(db: Session, budget: Budget) -> float:
    q = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == TransactionType.expense,
        extract("year", Transaction.date) == budget.year,
    )
    if budget.period_type.value == "monthly" and budget.month is not None:
        q = q.filter(extract("month", Transaction.date) == budget.month)
    if budget.scope_type.value == "category" and budget.category_id:
        q = q.filter(Transaction.category_id == budget.category_id)
    elif budget.scope_type.value == "account" and budget.account_id:
        q = q.filter(Transaction.account_id == budget.account_id)
    return float(q.scalar() or Decimal(0))


def get_dashboard_summary(db: Session) -> DashboardSummary:
    accounts = db.query(Account).order_by(Account.created_at).all()
    balances = get_all_account_balances(db, accounts)
    account_summaries = [
        AccountSummary(
            id=a.id,
            name=a.name,
            currency=a.currency,
            current_balance=balances[a.id],
        )
        for a in accounts
    ]

    rows = db.query(
        func.to_char(Transaction.date, "YYYY-MM").label("month"),
        func.sum(
            case((Transaction.type == TransactionType.income, Transaction.amount), else_=0)
        ).label("income"),
        func.sum(
            case((Transaction.type == TransactionType.expense, Transaction.amount), else_=0)
        ).label("expense"),
    ).group_by("month").order_by("month").all()

    cashflow = [
        MonthlyCashflow(month=r.month, income=float(r.income or 0), expense=float(r.expense or 0))
        for r in rows
    ]

    budgets = db.query(Budget).all()
    budget_progress = [
        BudgetProgress(
            budget_id=b.id,
            name=b.name,
            limit_amount=float(b.limit_amount),
            spent=get_budget_spent(db, b),
            currency=b.currency,
        )
        for b in budgets
    ]

    recent = (
        db.query(Transaction)
        .order_by(Transaction.date.desc(), Transaction.created_at.desc())
        .limit(10)
        .all()
    )

    return DashboardSummary(
        accounts=account_summaries,
        monthly_cashflow=cashflow,
        budget_progress=budget_progress,
        recent_transactions=[TransactionOut.model_validate(t) for t in recent],
    )

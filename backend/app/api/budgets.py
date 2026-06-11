from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.core.limiter import limiter
from app.core.security import get_current_session
from app.db.session import get_db
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetOut, BudgetUpdate
from app.services.dashboard import get_budget_spent

router = APIRouter(
    prefix="/budgets",
    tags=["budgets"],
    dependencies=[Depends(get_current_session)],
)


def _with_spent(budget: Budget, db: Session) -> BudgetOut:
    return BudgetOut(
        **{c.name: getattr(budget, c.name) for c in budget.__table__.columns},
        spent=get_budget_spent(db, budget),
    )


@router.get("", response_model=list[BudgetOut])
def list_budgets(
    skip: int = 0,
    limit: int = Query(default=100, le=500),
    db: Session = Depends(get_db),
):
    budgets = db.query(Budget).order_by(Budget.year.desc(), Budget.month.desc()).offset(skip).limit(limit).all()
    return [_with_spent(b, db) for b in budgets]


@router.get("/{budget_id}", response_model=BudgetOut)
def get_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = db.get(Budget, budget_id)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return _with_spent(budget, db)


@router.post("", response_model=BudgetOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("60/minute")
def create_budget(request: Request, body: BudgetCreate, db: Session = Depends(get_db)):
    budget = Budget(**body.model_dump())
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return _with_spent(budget, db)


@router.patch("/{budget_id}", response_model=BudgetOut)
def update_budget(budget_id: int, body: BudgetUpdate, db: Session = Depends(get_db)):
    budget = db.get(Budget, budget_id)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(budget, key, value)
    db.commit()
    db.refresh(budget)
    return _with_spent(budget, db)


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = db.get(Budget, budget_id)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    db.delete(budget)
    db.commit()

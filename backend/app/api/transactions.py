from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.core.limiter import limiter
from app.core.security import get_current_session
from app.db.session import get_db
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate, TransactionOut, TransactionUpdate

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    dependencies=[Depends(get_current_session)],
)


@router.get("", response_model=list[TransactionOut])
def list_transactions(
    account_id: int | None = Query(None),
    category_id: int | None = Query(None),
    type: TransactionType | None = Query(None),
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    skip: int = 0,
    limit: int = Query(default=100, le=1000),
    db: Session = Depends(get_db),
):
    q = db.query(Transaction)
    if account_id is not None:
        q = q.filter(Transaction.account_id == account_id)
    if category_id is not None:
        q = q.filter(Transaction.category_id == category_id)
    if type is not None:
        q = q.filter(Transaction.type == type)
    if date_from is not None:
        q = q.filter(Transaction.date >= date_from)
    if date_to is not None:
        q = q.filter(Transaction.date <= date_to)
    return q.order_by(Transaction.date.desc(), Transaction.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction


@router.post("", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("120/minute")
def create_transaction(request: Request, body: TransactionCreate, db: Session = Depends(get_db)):
    transaction = Transaction(**body.model_dump(), is_recurring=False)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.patch("/{transaction_id}", response_model=TransactionOut)
def update_transaction(transaction_id: int, body: TransactionUpdate, db: Session = Depends(get_db)):
    transaction = db.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(transaction, key, value)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    db.delete(transaction)
    db.commit()

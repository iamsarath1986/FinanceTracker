from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_session
from app.db.session import get_db
from app.models.account import Account
from app.schemas.account import AccountOut, AccountCreate, AccountUpdate

router = APIRouter(prefix="/accounts", tags=["accounts"], dependencies=[Depends(get_current_session)],)

def _with_balance(account: Account)-> AccountOut:
    # current_balance will include transactions once that model exists
    return AccountOut(
        **{c.name: getattr(account, c.name) for c in account.__table__.columns}, current_balance=float(
            account.opening_balance),
    )

@router.get("", response_model=list[AccountOut])
def list_accounts(db: Session = Depends(get_db)):
    accounts = db.query(Account).order_by(Account.created_at).all()
    return [_with_balance(a) for a in accounts]

@router.get("/{account_id}", response_model=AccountOut)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return _with_balance(account)

@router.post("", response_model=AccountOut, status_code=status.HTTP_201_CREATED)
def create_account(body: AccountCreate, db: Session = Depends(get_db)):
    account = Account(**body.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)
    return _with_balance(account)

@router.patch("/{account_id}", response_model=AccountOut, status_code=status.HTTP_200_OK)
def update_account(account_id: int, body: AccountUpdate, db: Session = Depends(get_db)):
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(account, key, value)
    db.commit()
    db.refresh(account)
    return _with_balance(account)

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    db.delete(account)
    db.commit()
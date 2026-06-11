from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.core.limiter import limiter
from app.core.security import get_current_session
from app.db.session import get_db
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountOut, AccountUpdate
from app.services.dashboard import get_account_balance, get_all_account_balances

router = APIRouter(prefix="/accounts", tags=["accounts"], dependencies=[Depends(get_current_session)])


def _with_balance(account: Account, db: Session) -> AccountOut:
    return AccountOut(
        **{c.name: getattr(account, c.name) for c in account.__table__.columns},
        current_balance=get_account_balance(db, account),
    )


@router.get("", response_model=list[AccountOut])
def list_accounts(
    skip: int = 0,
    limit: int = Query(default=100, le=1000),
    db: Session = Depends(get_db),
):
    accounts = db.query(Account).order_by(Account.created_at).offset(skip).limit(limit).all()
    balances = get_all_account_balances(db, accounts)
    return [
        AccountOut(
            **{c.name: getattr(a, c.name) for c in a.__table__.columns},
            current_balance=balances[a.id],
        )
        for a in accounts
    ]


@router.get("/{account_id}", response_model=AccountOut)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return _with_balance(account, db)


@router.post("", response_model=AccountOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("60/minute")
def create_account(request: Request, body: AccountCreate, db: Session = Depends(get_db)):
    account = Account(**body.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)
    return _with_balance(account, db)


@router.patch("/{account_id}", response_model=AccountOut)
def update_account(account_id: int, body: AccountUpdate, db: Session = Depends(get_db)):
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(account, key, value)
    db.commit()
    db.refresh(account)
    return _with_balance(account, db)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    db.delete(account)
    db.commit()

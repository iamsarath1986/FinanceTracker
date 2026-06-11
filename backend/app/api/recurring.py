from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.core.limiter import limiter
from app.core.security import get_current_session
from app.db.session import get_db
from app.models.recurring import RecurringTransaction
from app.schemas.recurring import RecurringCreate, RecurringOut, RecurringUpdate
from app.services.recurring import generate_due

router = APIRouter(
    prefix="/recurring",
    tags=["recurring"],
    dependencies=[Depends(get_current_session)],
)


@router.get("", response_model=list[RecurringOut])
def list_recurring(
    skip: int = 0,
    limit: int = Query(default=100, le=500),
    db: Session = Depends(get_db),
):
    return db.query(RecurringTransaction).order_by(RecurringTransaction.created_at).offset(skip).limit(limit).all()


@router.get("/{recurring_id}", response_model=RecurringOut)
def get_recurring(recurring_id: int, db: Session = Depends(get_db)):
    rec = db.get(RecurringTransaction, recurring_id)
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recurring transaction not found")
    return rec


@router.post("", response_model=RecurringOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("60/minute")
def create_recurring(request: Request, body: RecurringCreate, db: Session = Depends(get_db)):
    rec = RecurringTransaction(**body.model_dump())
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


@router.patch("/{recurring_id}", response_model=RecurringOut)
def update_recurring(recurring_id: int, body: RecurringUpdate, db: Session = Depends(get_db)):
    rec = db.get(RecurringTransaction, recurring_id)
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recurring transaction not found")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(rec, key, value)
    db.commit()
    db.refresh(rec)
    return rec


@router.delete("/{recurring_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recurring(recurring_id: int, db: Session = Depends(get_db)):
    rec = db.get(RecurringTransaction, recurring_id)
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recurring transaction not found")
    db.delete(rec)
    db.commit()


@router.post("/{recurring_id}/generate")
def trigger_generate(recurring_id: int, db: Session = Depends(get_db)):
    rec = db.get(RecurringTransaction, recurring_id)
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recurring transaction not found")
    generated = generate_due(db, recurring_id)
    return {"generated": generated}

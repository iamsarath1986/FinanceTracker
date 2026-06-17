import calendar
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.recurring import Frequency, RecurringTransaction
from app.models.transaction import Transaction


def _next_date(d: date, freq: Frequency) -> date:
    if freq == Frequency.daily:
        return d + timedelta(days=1)
    if freq == Frequency.weekly:
        return d + timedelta(weeks=1)
    if freq == Frequency.monthly:
        m = d.month % 12 + 1
        y = d.year + (d.month // 12)
        return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))
    # yearly
    y = d.year + 1
    return date(y, d.month, min(d.day, calendar.monthrange(y, d.month)[1]))


def generate_due(db: Session, recurring_id: int) -> int:
    rec = db.get(RecurringTransaction, recurring_id)
    if not rec or not rec.is_active:
        return 0

    start = rec.last_generated_date or rec.start_date
    today = date.today()

    if start > today:
        return 0

    generated = 0
    current = _next_date(start, rec.frequency)

    while current <= today:
        if rec.end_date and current > rec.end_date:
            break
        db.add(Transaction(
            account_id=rec.account_id,
            category_id=rec.category_id,
            amount=rec.amount,
            type=rec.type,
            date=current,
            description=rec.description,
            is_recurring=True,
            recurring_id=rec.id,
        ))
        rec.last_generated_date = current
        generated += 1
        current = _next_date(current, rec.frequency)

    if generated:
        db.commit()

    return generated


def generate_all_due(db: Session) -> None:
    recs = db.query(RecurringTransaction).filter(RecurringTransaction.is_active == True).all()
    for rec in recs:
        generate_due(db, rec.id)

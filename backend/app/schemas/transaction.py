import datetime as dt

from pydantic import BaseModel, ConfigDict, Field

from app.models.transaction import TransactionType


class TransactionCreate(BaseModel):
    account_id: int
    category_id: int | None = None
    amount: float = Field(gt=0)
    type: TransactionType
    date: dt.date
    description: str | None = None


class TransactionUpdate(BaseModel):
    account_id: int | None = None
    category_id: int | None = None
    amount: float | None = Field(None, gt=0)
    type: TransactionType | None = None
    date: dt.date | None = None
    description: str | None = None


class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    account_id: int
    category_id: int | None
    amount: float
    type: TransactionType
    date: dt.date
    description: str | None
    is_recurring: bool
    recurring_id: int | None
    created_at: dt.datetime

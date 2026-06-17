from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.recurring import Frequency
from app.models.transaction import TransactionType


class RecurringCreate(BaseModel):
    account_id: int
    category_id: int | None = None
    amount: float = Field(gt=0)
    type: TransactionType
    description: str | None = None
    frequency: Frequency
    start_date: date
    end_date: date | None = None
    is_active: bool = True

    @model_validator(mode="after")
    def validate_dates(self) -> "RecurringCreate":
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self


class RecurringUpdate(BaseModel):
    account_id: int | None = None
    category_id: int | None = None
    amount: float | None = Field(None, gt=0)
    type: TransactionType | None = None
    description: str | None = None
    frequency: Frequency | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_active: bool | None = None


class RecurringOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    account_id: int
    category_id: int | None
    amount: float
    type: TransactionType
    description: str | None
    frequency: Frequency
    start_date: date
    end_date: date | None
    last_generated_date: date | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

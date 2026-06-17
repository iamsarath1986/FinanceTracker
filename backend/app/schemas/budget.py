from pydantic import BaseModel, ConfigDict, Field

from app.models.budget import PeriodType, ScopeType


class BudgetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    scope_type: ScopeType
    period_type: PeriodType
    category_id: int | None = None
    account_id: int | None = None
    year: int = Field(ge=2000, le=2100)
    month: int | None = Field(None, ge=1, le=12)
    limit_amount: float = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)


class BudgetUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    limit_amount: float | None = Field(None, gt=0)
    currency: str | None = Field(None, min_length=3, max_length=3)


class BudgetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    scope_type: ScopeType
    period_type: PeriodType
    category_id: int | None
    account_id: int | None
    year: int
    month: int | None
    limit_amount: float
    currency: str
    spent: float

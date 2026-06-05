from datetime import datetime
from app.models.account import AccountType
from pydantic import BaseModel, ConfigDict

class AccountCreate(BaseModel):
    name: str
    type: AccountType
    bank_name: str | None = None
    country: str | None = None
    currency: str
    opening_balance: float = 0

class AccountUpdate(BaseModel):
    name: str | None = None
    type: AccountType | None = None
    bank_name: str | None = None
    country: str | None = None
    currency: str | None = None
    opening_balance: float | None = None

class AccountOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: AccountType
    bank_name: str | None
    country: str | None
    currency: str
    opening_balance: float
    current_balance: float
    created_at: datetime
    updated_at: datetime
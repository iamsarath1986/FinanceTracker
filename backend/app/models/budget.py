import enum

from sqlalchemy import Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class ScopeType(str, enum.Enum):
    category = "category"
    account = "account"


class PeriodType(str, enum.Enum):
    monthly = "monthly"
    annual = "annual"


class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    scope_type: Mapped[ScopeType] = mapped_column(Enum(ScopeType, name="scope_type"))
    period_type: Mapped[PeriodType] = mapped_column(Enum(PeriodType, name="period_type"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"))
    account_id: Mapped[int | None] = mapped_column(ForeignKey("accounts.id", ondelete="SET NULL"))
    year: Mapped[int] = mapped_column(Integer)
    month: Mapped[int | None] = mapped_column(Integer)
    limit_amount: Mapped[float] = mapped_column(Numeric(15, 2))
    currency: Mapped[str] = mapped_column(String(3))

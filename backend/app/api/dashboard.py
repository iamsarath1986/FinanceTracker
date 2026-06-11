from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_session
from app.db.session import get_db
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard import get_dashboard_summary
from app.services.recurring import generate_all_due

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    dependencies=[Depends(get_current_session)],
)


@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db)):
    generate_all_due(db)
    return get_dashboard_summary(db)

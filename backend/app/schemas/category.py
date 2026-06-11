from datetime import datetime

from app.models.category import CategoryType
from pydantic import BaseModel, ConfigDict

class CategoryCreate(BaseModel):
    name: str
    type: CategoryType
    color: str | None = None
    icon: str | None = None

class CategoryUpdate(BaseModel):
    name: str | None = None
    type: CategoryType | None = None
    color: str | None = None
    icon: str | None = None

class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: CategoryType
    color: str | None
    icon: str | None
    created_at: datetime
    updated_at: datetime
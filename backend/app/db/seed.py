from sqlalchemy.orm import Session
from app.models.category import Category, CategoryType

DEFAULT_CATEGORIES = [
    {"name": "Salary",          "type": CategoryType.income,  "color": "#22c55e", "icon": "pi pi-briefcase"},
    {"name": "Freelance",       "type": CategoryType.income,  "color": "#16a34a", "icon": "pi pi-desktop"},
    {"name": "Investment",      "type": CategoryType.income,  "color": "#15803d", "icon": "pi pi-chart-line"},
    {"name": "Other Income",    "type": CategoryType.income,  "color": "#86efac", "icon": "pi pi-plus-circle"},
    {"name": "Food",            "type": CategoryType.expense, "color": "#f97316", "icon": "pi pi-shopping-cart"},
    {"name": "Transport",       "type": CategoryType.expense, "color": "#eab308", "icon": "pi pi-car"},
    {"name": "Housing",         "type": CategoryType.expense, "color": "#ef4444", "icon": "pi pi-home"},
    {"name": "Utilities",       "type": CategoryType.expense, "color": "#ec4899", "icon": "pi pi-bolt"},
    {"name": "Healthcare",      "type": CategoryType.expense, "color": "#a855f7", "icon": "pi pi-heart"},
    {"name": "Entertainment",   "type": CategoryType.expense, "color": "#3b82f6", "icon": "pi pi-star"},
    {"name": "Shopping",        "type": CategoryType.expense, "color": "#06b6d4", "icon": "pi pi-tag"},
    {"name": "Education",       "type": CategoryType.expense, "color": "#8b5cf6", "icon": "pi pi-book"},
    {"name": "Other Expense",   "type": CategoryType.expense, "color": "#94a3b8", "icon": "pi pi-minus-circle"},
]


def seed_categories(db: Session) -> None:
    if db.query(Category).first():
        return
    db.add_all([Category(**c) for c in DEFAULT_CATEGORIES])
    db.commit()

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime
from decimal import Decimal
from app.database import get_db
from app.models import User, Expense, Category, Budget
from app.schemas.dashboard import DashboardResponse, CategoryBreakdown, TrendData
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])

@router.get("", response_model=DashboardResponse)
async def get_dashboard(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    month: int = Query(None),
    year: int = Query(None)
):
    today = date.today()
    if month is None:
        month = today.month
    if year is None:
        year = today.year

    # Déterminer les dates
    if month == 1:
        start_date = date(year - 1, 12, 1)
    else:
        start_date = date(year, month - 1, 1)

    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    current_start = date(year, month, 1)
    if month == 12:
        current_end = date(year + 1, 1, 1)
    else:
        current_end = date(year, month + 1, 1)

    # Stats du mois courant
    total_month = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user.user_id,
        Expense.date >= current_start,
        Expense.date < current_end
    ).scalar() or Decimal(0)

    today_sum = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user.user_id,
        Expense.date == today
    ).scalar() or Decimal(0)

    # Répartition par catégorie (mois courant)
    category_breakdown = db.query(
        Category.category_id,
        Category.name,
        Category.emoji,
        Category.color,
        func.sum(Expense.amount).label('total')
    ).join(Expense).filter(
        Expense.user_id == user.user_id,
        Expense.date >= current_start,
        Expense.date < current_end
    ).group_by(
        Category.category_id, Category.name, Category.emoji, Category.color
    ).all()

    total_by_category = sum([item[4] for item in category_breakdown])
    breakdown = [
        CategoryBreakdown(
            category_id=str(item[0]),
            category_name=item[1],
            emoji=item[2],
            color=item[3],
            amount=item[4],
            percentage=float((item[4] / total_by_category * 100) if total_by_category > 0 else 0)
        )
        for item in category_breakdown
    ]

    # Tendance 6 mois
    trend_data = []
    for i in range(6):
        if month - i <= 0:
            m = 12 + (month - i)
            y = year - 1
        else:
            m = month - i
            y = year

        month_start = date(y, m, 1)
        if m == 12:
            month_end = date(y + 1, 1, 1)
        else:
            month_end = date(y, m + 1, 1)

        amount = db.query(func.sum(Expense.amount)).filter(
            Expense.user_id == user.user_id,
            Expense.date >= month_start,
            Expense.date < month_end
        ).scalar() or Decimal(0)

        trend_data.insert(0, TrendData(month=m, year=y, amount=amount))

    # Budget résumé
    budgets = db.query(Budget).filter(Budget.user_id == user.user_id).all()
    budget_summary = {
        "total_budgets": len(budgets),
        "budgets_alert": 0,
        "budgets_exceeded": 0
    }

    for budget in budgets:
        spent = db.query(func.sum(Expense.amount)).filter(
            Expense.category_id == budget.category_id,
            Expense.date >= current_start,
            Expense.date < current_end
        ).scalar() or Decimal(0)

        percentage = float((spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0)
        if percentage >= budget.alert_threshold:
            budget_summary["budgets_alert"] += 1
        if percentage >= 100:
            budget_summary["budgets_exceeded"] += 1

    return DashboardResponse(
        stats={
            "total": str(total_month),
            "today": str(today_sum),
            "month": month,
            "year": year,
            "currency": "DH"
        },
        breakdown=breakdown,
        trend=trend_data,
        budget_summary=budget_summary
    )

@router.get("/summary")
async def get_summary(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    today = date.today()

    # Aujourd'hui
    today_sum = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user.user_id,
        Expense.date == today
    ).scalar() or Decimal(0)

    # Ce mois
    month_start = date(today.year, today.month, 1)
    if today.month == 12:
        month_end = date(today.year + 1, 1, 1)
    else:
        month_end = date(today.year, today.month + 1, 1)

    month_sum = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user.user_id,
        Expense.date >= month_start,
        Expense.date < month_end
    ).scalar() or Decimal(0)

    # Cette année
    year_start = date(today.year, 1, 1)
    year_end = date(today.year + 1, 1, 1)

    year_sum = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user.user_id,
        Expense.date >= year_start,
        Expense.date < year_end
    ).scalar() or Decimal(0)

    return {
        "today": str(today_sum),
        "month": str(month_sum),
        "year": str(year_sum),
        "currency": "DH"
    }

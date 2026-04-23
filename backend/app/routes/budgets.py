from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from datetime import date
from decimal import Decimal
from app.database import get_db
from app.models import User, Budget, Category, Expense
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse, BudgetWithStatus
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/budgets", tags=["budgets"])

def calculate_budget_status(budget: Budget, db: Session, month: int = None, year: int = None):
    if month is None or year is None:
        today = date.today()
        month = today.month
        year = today.year

    # Calculer les dépenses du mois pour cette catégorie
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    spent_result = db.query(func.sum(Expense.amount)).filter(
        Expense.category_id == budget.category_id,
        Expense.date >= start_date,
        Expense.date < end_date
    ).scalar()

    spent = Decimal(spent_result or 0)
    percentage = float((spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0)
    is_alert = percentage >= budget.alert_threshold
    is_exceeded = percentage >= 100

    return BudgetWithStatus(
        budget_id=budget.budget_id,
        user_id=budget.user_id,
        category_id=budget.category_id,
        monthly_limit=budget.monthly_limit,
        alert_threshold=budget.alert_threshold,
        created_at=budget.created_at,
        updated_at=budget.updated_at,
        spent=spent,
        percentage=percentage,
        is_alert=is_alert,
        is_exceeded=is_exceeded
    )

@router.post("", response_model=BudgetResponse)
async def create_budget(
    budget_data: BudgetCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Vérifier que la catégorie appartient à l'utilisateur
    category = db.query(Category).filter(
        Category.category_id == budget_data.category_id,
        Category.user_id == user.user_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Vérifier qu'un budget n'existe pas déjà pour cette catégorie
    existing_budget = db.query(Budget).filter(
        Budget.category_id == budget_data.category_id,
        Budget.user_id == user.user_id
    ).first()

    if existing_budget:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Budget already exists for this category"
        )

    budget = Budget(
        user_id=user.user_id,
        category_id=budget_data.category_id,
        monthly_limit=budget_data.monthly_limit,
        alert_threshold=budget_data.alert_threshold
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return BudgetResponse.from_orm(budget)

@router.get("", response_model=list[BudgetWithStatus])
async def list_budgets(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    month: int = Query(None),
    year: int = Query(None)
):
    budgets = db.query(Budget).filter(Budget.user_id == user.user_id).all()
    return [calculate_budget_status(b, db, month, year) for b in budgets]

@router.get("/{budget_id}", response_model=BudgetWithStatus)
async def get_budget(
    budget_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    month: int = Query(None),
    year: int = Query(None)
):
    budget = db.query(Budget).filter(
        Budget.budget_id == budget_id,
        Budget.user_id == user.user_id
    ).first()

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )

    return calculate_budget_status(budget, db, month, year)

@router.put("/{budget_id}", response_model=BudgetResponse)
async def update_budget(
    budget_id: UUID,
    budget_data: BudgetUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    budget = db.query(Budget).filter(
        Budget.budget_id == budget_id,
        Budget.user_id == user.user_id
    ).first()

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )

    if budget_data.monthly_limit:
        budget.monthly_limit = budget_data.monthly_limit
    if budget_data.alert_threshold:
        budget.alert_threshold = budget_data.alert_threshold

    db.commit()
    db.refresh(budget)
    return BudgetResponse.from_orm(budget)

@router.delete("/{budget_id}")
async def delete_budget(
    budget_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    budget = db.query(Budget).filter(
        Budget.budget_id == budget_id,
        Budget.user_id == user.user_id
    ).first()

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )

    db.delete(budget)
    db.commit()
    return {"message": "Budget deleted"}

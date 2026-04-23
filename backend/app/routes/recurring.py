from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import User, RecurringExpense, Expense, Category
from app.schemas.recurring import RecurringExpenseCreate, RecurringExpenseUpdate, RecurringExpenseResponse
from app.dependencies import get_current_user
from decimal import Decimal
from datetime import date

router = APIRouter(prefix="/api/v1/recurring", tags=["recurring"])

@router.post("", response_model=RecurringExpenseResponse)
async def create_recurring_expense(
    recurring_data: RecurringExpenseCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Vérifier que la catégorie appartient à l'utilisateur
    category = db.query(Category).filter(
        Category.category_id == recurring_data.category_id,
        Category.user_id == user.user_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Créer la dépense (template)
    expense = Expense(
        user_id=user.user_id,
        category_id=recurring_data.category_id,
        title=recurring_data.title,
        amount=Decimal(str(recurring_data.amount)),
        date=date.today(),
        is_recurring=True
    )
    db.add(expense)
    db.flush()

    # Créer la dépense récurrente
    recurring = RecurringExpense(
        user_id=user.user_id,
        expense_id=expense.expense_id,
        frequency=recurring_data.frequency,
        is_active=True,
        last_execution_date=None
    )
    db.add(recurring)
    db.commit()
    db.refresh(recurring)
    return RecurringExpenseResponse.from_orm(recurring)

@router.get("", response_model=list[RecurringExpenseResponse])
async def list_recurring_expenses(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recurring_expenses = db.query(RecurringExpense).filter(
        RecurringExpense.user_id == user.user_id
    ).all()
    return [RecurringExpenseResponse.from_orm(r) for r in recurring_expenses]

@router.get("/{recurring_id}", response_model=RecurringExpenseResponse)
async def get_recurring_expense(
    recurring_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recurring = db.query(RecurringExpense).filter(
        RecurringExpense.recurring_id == recurring_id,
        RecurringExpense.user_id == user.user_id
    ).first()

    if not recurring:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring expense not found"
        )

    return RecurringExpenseResponse.from_orm(recurring)

@router.put("/{recurring_id}", response_model=RecurringExpenseResponse)
async def update_recurring_expense(
    recurring_id: UUID,
    recurring_data: RecurringExpenseUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recurring = db.query(RecurringExpense).filter(
        RecurringExpense.recurring_id == recurring_id,
        RecurringExpense.user_id == user.user_id
    ).first()

    if not recurring:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring expense not found"
        )

    if recurring_data.frequency:
        recurring.frequency = recurring_data.frequency

    if recurring_data.is_active is not None:
        recurring.is_active = recurring_data.is_active

    # Mettre à jour la dépense associée
    expense = recurring.expense
    if recurring_data.title:
        expense.title = recurring_data.title
    if recurring_data.amount:
        expense.amount = Decimal(str(recurring_data.amount))
    if recurring_data.category_id:
        category = db.query(Category).filter(
            Category.category_id == recurring_data.category_id,
            Category.user_id == user.user_id
        ).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        expense.category_id = recurring_data.category_id

    db.commit()
    db.refresh(recurring)
    return RecurringExpenseResponse.from_orm(recurring)

@router.delete("/{recurring_id}")
async def delete_recurring_expense(
    recurring_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recurring = db.query(RecurringExpense).filter(
        RecurringExpense.recurring_id == recurring_id,
        RecurringExpense.user_id == user.user_id
    ).first()

    if not recurring:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring expense not found"
        )

    # Supprimer la dépense et le recurring
    db.delete(recurring)
    db.delete(recurring.expense)
    db.commit()
    return {"message": "Recurring expense deleted"}

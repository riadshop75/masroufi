from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date
from app.database import get_db
from app.models import User, Expense, Category
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/expenses", tags=["expenses"])

@router.post("", response_model=ExpenseResponse)
async def create_expense(
    expense_data: ExpenseCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Vérifier que la catégorie appartient à l'utilisateur
    category = db.query(Category).filter(
        Category.category_id == expense_data.category_id,
        Category.user_id == user.user_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    expense = Expense(
        user_id=user.user_id,
        category_id=expense_data.category_id,
        title=expense_data.title,
        amount=expense_data.amount,
        date=expense_data.date,
        note=expense_data.note,
        is_recurring=False
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return ExpenseResponse.from_orm(expense)

@router.get("", response_model=list[ExpenseResponse])
async def list_expenses(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    month: int = Query(None),
    year: int = Query(None),
    category_id: UUID = Query(None)
):
    query = db.query(Expense).filter(Expense.user_id == user.user_id)

    if category_id:
        query = query.filter(Expense.category_id == category_id)

    if month and year:
        query = query.filter(
            Expense.date >= date(year, month, 1),
            Expense.date < date(year, month + 1 if month < 12 else 1, 1)
        )

    expenses = query.order_by(Expense.date.desc()).all()
    return [ExpenseResponse.from_orm(e) for e in expenses]

@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(
    expense_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expense = db.query(Expense).filter(
        Expense.expense_id == expense_id,
        Expense.user_id == user.user_id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    return ExpenseResponse.from_orm(expense)

@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: UUID,
    expense_data: ExpenseUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expense = db.query(Expense).filter(
        Expense.expense_id == expense_id,
        Expense.user_id == user.user_id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    # Vérifier la catégorie si modifiée
    if expense_data.category_id:
        category = db.query(Category).filter(
            Category.category_id == expense_data.category_id,
            Category.user_id == user.user_id
        ).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        expense.category_id = expense_data.category_id

    if expense_data.title:
        expense.title = expense_data.title
    if expense_data.amount:
        expense.amount = expense_data.amount
    if expense_data.date:
        expense.date = expense_data.date
    if expense_data.note is not None:
        expense.note = expense_data.note

    db.commit()
    db.refresh(expense)
    return ExpenseResponse.from_orm(expense)

@router.delete("/{expense_id}")
async def delete_expense(
    expense_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expense = db.query(Expense).filter(
        Expense.expense_id == expense_id,
        Expense.user_id == user.user_id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted"}

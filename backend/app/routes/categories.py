from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import User, Category, Expense
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, DefaultCategory
from app.dependencies import get_current_user

DEFAULT_CATEGORIES = [
    DefaultCategory(name="Alimentation", emoji="🍕", color="#FF6B6B"),
    DefaultCategory(name="Transport", emoji="🚗", color="#4ECDC4"),
    DefaultCategory(name="Loisirs", emoji="🎮", color="#95E1D3"),
    DefaultCategory(name="Santé", emoji="🏥", color="#FFE66D"),
    DefaultCategory(name="Shopping", emoji="🛍️", color="#FF6B9D"),
    DefaultCategory(name="Maison", emoji="🏠", color="#C7CEEA"),
    DefaultCategory(name="Travail", emoji="💼", color="#B4A7D6"),
    DefaultCategory(name="Autre", emoji="📌", color="#95E1D3"),
]

router = APIRouter(prefix="/api/v1/categories", tags=["categories"])

@router.post("", response_model=CategoryResponse)
async def create_category(
    category_data: CategoryCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category = Category(
        user_id=user.user_id,
        name=category_data.name,
        emoji=category_data.emoji,
        color=category_data.color
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return CategoryResponse.from_orm(category)

@router.get("", response_model=list[CategoryResponse])
async def list_categories(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    categories = db.query(Category).filter(Category.user_id == user.user_id).all()
    return [CategoryResponse.from_orm(c) for c in categories]

@router.post("/init-defaults")
async def init_default_categories(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(Category).filter(Category.user_id == user.user_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has categories"
        )

    for default_cat in DEFAULT_CATEGORIES:
        category = Category(
            user_id=user.user_id,
            name=default_cat.name,
            emoji=default_cat.emoji,
            color=default_cat.color
        )
        db.add(category)

    db.commit()
    categories = db.query(Category).filter(Category.user_id == user.user_id).all()
    return [CategoryResponse.from_orm(c) for c in categories]

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.category_id == category_id,
        Category.user_id == user.user_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return CategoryResponse.from_orm(category)

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.category_id == category_id,
        Category.user_id == user.user_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    if category_data.name:
        category.name = category_data.name
    if category_data.emoji:
        category.emoji = category_data.emoji
    if category_data.color:
        category.color = category_data.color

    db.commit()
    db.refresh(category)
    return CategoryResponse.from_orm(category)

@router.delete("/{category_id}")
async def delete_category(
    category_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.category_id == category_id,
        Category.user_id == user.user_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Vérifier s'il y a des dépenses liées
    expenses_count = db.query(Expense).filter(Expense.category_id == category_id).count()
    if expenses_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete category with {expenses_count} expenses. Please delete them first or change their category."
        )

    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}

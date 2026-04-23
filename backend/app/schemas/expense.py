from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    amount: Decimal = Field(..., gt=0)
    category_id: UUID
    date: date = Field(default_factory=date.today)
    note: Optional[str] = Field(None, max_length=1000)

class ExpenseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[Decimal] = Field(None, gt=0)
    category_id: Optional[UUID] = None
    date: Optional[date] = None
    note: Optional[str] = Field(None, max_length=1000)

class ExpenseResponse(BaseModel):
    expense_id: UUID
    user_id: UUID
    category_id: UUID
    title: str
    amount: Decimal
    date: date
    note: Optional[str]
    is_recurring: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

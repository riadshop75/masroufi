from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime, date
from typing import Optional, Literal

class RecurringExpenseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    amount: float = Field(..., gt=0)
    category_id: UUID
    frequency: Literal["weekly", "monthly", "yearly"]

class RecurringExpenseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[float] = Field(None, gt=0)
    category_id: Optional[UUID] = None
    frequency: Optional[Literal["weekly", "monthly", "yearly"]] = None
    is_active: Optional[bool] = None

class RecurringExpenseResponse(BaseModel):
    recurring_id: UUID
    user_id: UUID
    expense_id: UUID
    frequency: str
    is_active: bool
    last_execution_date: Optional[date]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

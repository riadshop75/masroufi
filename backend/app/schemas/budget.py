from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional

class BudgetCreate(BaseModel):
    category_id: UUID
    monthly_limit: Decimal = Field(..., gt=0)
    alert_threshold: int = Field(default=80, ge=1, le=100)

class BudgetUpdate(BaseModel):
    monthly_limit: Optional[Decimal] = Field(None, gt=0)
    alert_threshold: Optional[int] = Field(None, ge=1, le=100)

class BudgetResponse(BaseModel):
    budget_id: UUID
    user_id: UUID
    category_id: UUID
    monthly_limit: Decimal
    alert_threshold: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BudgetWithStatus(BudgetResponse):
    spent: Decimal
    percentage: float
    is_alert: bool
    is_exceeded: bool

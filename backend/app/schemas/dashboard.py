from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional, Dict, List

class DashboardStat(BaseModel):
    label: str
    value: Decimal
    currency: str = "DH"

class CategoryBreakdown(BaseModel):
    category_id: str
    category_name: str
    emoji: Optional[str]
    color: str
    amount: Decimal
    percentage: float

class TrendData(BaseModel):
    month: int
    year: int
    amount: Decimal

class DashboardResponse(BaseModel):
    stats: Dict[str, any]
    breakdown: List[CategoryBreakdown]
    trend: List[TrendData]
    budget_summary: Optional[Dict[str, any]] = None

class ExportRequest(BaseModel):
    month: Optional[int] = None
    year: Optional[int] = None
    category_id: Optional[str] = None

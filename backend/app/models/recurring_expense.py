from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Date, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, date
import uuid
import enum
from app.database import Base

class FrequencyEnum(str, enum.Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class RecurringExpense(Base):
    __tablename__ = "recurring_expenses"

    recurring_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    expense_id = Column(UUID(as_uuid=True), ForeignKey("expenses.expense_id"), nullable=False, unique=True)
    frequency = Column(Enum(FrequencyEnum), nullable=False)
    is_active = Column(Boolean, default=True)
    last_execution_date = Column(Date, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="recurring_expenses")
    expense = relationship("Expense", back_populates="recurring_expense")

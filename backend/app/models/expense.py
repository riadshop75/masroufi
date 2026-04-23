from sqlalchemy import Column, String, DateTime, ForeignKey, Date, Numeric, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, date
import uuid
from app.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    expense_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.category_id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    date = Column(Date, nullable=False, index=True, default=date.today)
    note = Column(Text, nullable=True)
    is_recurring = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")
    recurring_expense = relationship("RecurringExpense", back_populates="expense", uselist=False, cascade="all, delete-orphan")

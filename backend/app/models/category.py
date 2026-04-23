from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    category_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    emoji = Column(String(10), nullable=True)
    color = Column(String(7), nullable=True, default="#1D4ED8")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="categories")
    expenses = relationship("Expense", back_populates="category", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="category", cascade="all, delete-orphan")

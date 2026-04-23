from sqlalchemy import Column, DateTime, ForeignKey, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

class Budget(Base):
    __tablename__ = "budgets"

    budget_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.category_id"), nullable=False, index=True)
    monthly_limit = Column(Numeric(10, 2), nullable=False)
    alert_threshold = Column(Integer, default=80, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")

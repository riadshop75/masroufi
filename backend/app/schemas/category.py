from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    emoji: Optional[str] = Field(None, max_length=10)
    color: str = Field(default="#1D4ED8", regex="^#[0-9A-Fa-f]{6}$")

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    emoji: Optional[str] = Field(None, max_length=10)
    color: Optional[str] = Field(None, regex="^#[0-9A-Fa-f]{6}$")

class CategoryResponse(BaseModel):
    category_id: UUID
    user_id: UUID
    name: str
    emoji: Optional[str]
    color: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DefaultCategory(BaseModel):
    name: str
    emoji: str
    color: str

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class ApiTokenCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    scopes: List[str] = Field(default=["read:expenses", "write:expenses"])

class ApiTokenResponse(BaseModel):
    token_id: UUID
    name: str
    scopes: List[str]
    is_active: bool
    last_used: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class ApiTokenWithSecret(ApiTokenResponse):
    token: str

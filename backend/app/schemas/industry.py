from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class IndustryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = Field(None, pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")  # Hex color validation
    sort_order: int = 0

class IndustryCreate(IndustryBase):
    pass

class IndustryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = Field(None, pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None

class IndustryResponse(IndustryBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    business_count: Optional[int] = 0  # Number of businesses in this industry
    
    class Config:
        from_attributes = True

class IndustryListResponse(BaseModel):
    id: int
    name: str
    slug: str
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: bool
    business_count: Optional[int] = 0
    
    class Config:
        from_attributes = True
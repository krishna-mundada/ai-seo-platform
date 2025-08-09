from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, List
from datetime import datetime

class BusinessBase(BaseModel):
    name: str
    industry: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    location: Optional[str] = None
    target_audience: Optional[str] = None

class BusinessCreate(BusinessBase):
    owner_id: int
    brand_voice: Optional[str] = None
    brand_guidelines: Optional[Dict] = None
    keywords: Optional[List[str]] = None
    competitors: Optional[List[str]] = None
    social_handles: Optional[Dict[str, str]] = None

class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    location: Optional[str] = None
    target_audience: Optional[str] = None
    brand_voice: Optional[str] = None
    brand_guidelines: Optional[Dict] = None
    keywords: Optional[List[str]] = None
    competitors: Optional[List[str]] = None
    social_handles: Optional[Dict[str, str]] = None

class BusinessResponse(BusinessBase):
    id: int
    owner_id: int
    brand_voice: Optional[str] = None
    brand_guidelines: Optional[Dict] = None
    keywords: Optional[List[str]] = None
    competitors: Optional[List[str]] = None
    social_handles: Optional[Dict[str, str]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
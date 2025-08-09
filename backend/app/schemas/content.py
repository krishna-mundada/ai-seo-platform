from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from app.models.content import ContentType, ContentStatus

class ContentBase(BaseModel):
    title: str
    content_text: str
    content_type: ContentType

class ContentCreate(ContentBase):
    business_id: int
    campaign_id: Optional[int] = None
    meta_description: Optional[str] = None
    keywords: Optional[List[str]] = None
    scheduled_publish_at: Optional[datetime] = None

class ContentGenerate(BaseModel):
    business_id: int
    content_type: ContentType
    topic: Optional[str] = None
    keywords: Optional[List[str]] = None
    campaign_id: Optional[int] = None

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    content_text: Optional[str] = None
    status: Optional[ContentStatus] = None
    meta_description: Optional[str] = None
    keywords: Optional[List[str]] = None
    scheduled_publish_at: Optional[datetime] = None

class BusinessInfo(BaseModel):
    id: int
    name: str
    industry: Optional[str] = None
    
    class Config:
        from_attributes = True

class ContentResponse(ContentBase):
    id: int
    business_id: int
    campaign_id: Optional[int] = None
    status: ContentStatus
    meta_description: Optional[str] = None
    keywords: Optional[List[str]] = None
    seo_score: Optional[int] = None
    scheduled_publish_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    platform_specific_data: Optional[Dict] = None
    ai_prompt_used: Optional[str] = None
    ai_model_used: Optional[str] = None
    generation_settings: Optional[Dict] = None
    views: int = 0
    clicks: int = 0
    engagement_rate: int = 0
    is_auto_generated: bool = True
    requires_approval: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
    business: Optional[BusinessInfo] = None
    
    class Config:
        from_attributes = True
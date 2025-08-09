from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from app.models.campaign import CampaignType, CampaignStatus

class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    campaign_type: CampaignType

class CampaignCreate(CampaignBase):
    business_id: int
    target_keywords: Optional[List[str]] = None
    target_platforms: Optional[List[str]] = None
    content_frequency: Optional[str] = None
    auto_generate_content: bool = True
    auto_publish: bool = False
    requires_approval: bool = True
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    target_keywords: Optional[List[str]] = None
    target_platforms: Optional[List[str]] = None
    content_frequency: Optional[str] = None
    auto_generate_content: Optional[bool] = None
    auto_publish: Optional[bool] = None
    requires_approval: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class CampaignResponse(CampaignBase):
    id: int
    business_id: int
    status: CampaignStatus
    target_keywords: Optional[List[str]] = None
    target_platforms: Optional[List[str]] = None
    content_frequency: Optional[str] = None
    auto_generate_content: bool = True
    auto_publish: bool = False
    requires_approval: bool = True
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    total_content_pieces: int = 0
    published_content: int = 0
    total_views: int = 0
    total_clicks: int = 0
    avg_engagement_rate: int = 0
    content_template: Optional[str] = None
    brand_voice_override: Optional[str] = None
    generation_settings: Optional[Dict] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
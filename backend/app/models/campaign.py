from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class CampaignStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class CampaignType(enum.Enum):
    CONTENT_SERIES = "content_series"  # Blog series
    SOCIAL_MEDIA = "social_media"      # Social media campaign
    SEO_BOOST = "seo_boost"            # SEO optimization campaign
    PRODUCT_LAUNCH = "product_launch"  # Product/service launch
    SEASONAL = "seasonal"              # Holiday/seasonal content
    CUSTOM = "custom"                  # Custom campaign

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    campaign_type = Column(Enum(CampaignType), nullable=False)
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)
    
    # Campaign settings
    target_keywords = Column(JSON, nullable=True)  # Primary keywords for campaign
    target_platforms = Column(JSON, nullable=True)  # ["linkedin", "twitter", "blog"]
    content_frequency = Column(String, nullable=True)  # "daily", "weekly", "bi-weekly"
    
    # AI automation settings
    auto_generate_content = Column(Boolean, default=True)
    auto_publish = Column(Boolean, default=False)
    requires_approval = Column(Boolean, default=True)
    
    # Campaign timeline
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    
    # Performance tracking
    total_content_pieces = Column(Integer, default=0)
    published_content = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    total_clicks = Column(Integer, default=0)
    avg_engagement_rate = Column(Integer, default=0)  # Stored as percentage * 100
    
    # AI generation settings
    content_template = Column(Text, nullable=True)  # Template for AI generation
    brand_voice_override = Column(Text, nullable=True)  # Campaign-specific brand voice
    generation_settings = Column(JSON, nullable=True)  # AI model settings
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    
    # Relationships
    business = relationship("Business", back_populates="campaigns")
    content = relationship("Content", back_populates="campaign")
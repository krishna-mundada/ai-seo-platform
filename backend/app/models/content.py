from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class ContentType(enum.Enum):
    BLOG_POST = "blog_post"
    LINKEDIN_POST = "linkedin_post"
    TWITTER_POST = "twitter_post"
    FACEBOOK_POST = "facebook_post"
    INSTAGRAM_POST = "instagram_post"
    REDDIT_POST = "reddit_post"
    QUORA_POST = "quora_post"
    EMAIL = "email"
    AD_COPY = "ad_copy"

class ContentStatus(enum.Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    PUBLISHED = "published"
    SCHEDULED = "scheduled"
    FAILED = "failed"

class Content(Base):
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content_text = Column(Text, nullable=False)
    content_type = Column(Enum(ContentType), nullable=False)
    status = Column(Enum(ContentStatus), default=ContentStatus.DRAFT)
    
    # SEO fields
    meta_description = Column(Text, nullable=True)
    keywords = Column(JSON, nullable=True)  # Target keywords for this content
    seo_score = Column(Integer, nullable=True)  # SEO optimization score
    
    # Publishing details
    scheduled_publish_at = Column(DateTime(timezone=True), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    platform_specific_data = Column(JSON, nullable=True)  # Platform-specific formatting
    
    # AI generation metadata
    ai_prompt_used = Column(Text, nullable=True)
    ai_model_used = Column(String, nullable=True)
    generation_settings = Column(JSON, nullable=True)
    
    # Performance tracking
    views = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    engagement_rate = Column(Integer, default=0)  # Stored as percentage * 100
    
    # Auto-generation flags
    is_auto_generated = Column(Boolean, default=True)
    requires_approval = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys with cascading delete
    business_id = Column(Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=True)
    
    # Relationships
    business = relationship("Business", back_populates="content")
    campaign = relationship("Campaign", back_populates="content")
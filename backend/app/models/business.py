from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Business(Base):
    __tablename__ = "businesses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    industry = Column(String, nullable=True)  # Legacy field - will be deprecated
    industry_id = Column(Integer, ForeignKey("industries.id"), nullable=True)
    description = Column(Text, nullable=True)
    website_url = Column(String, nullable=True)
    location = Column(String, nullable=True)
    target_audience = Column(Text, nullable=True)
    
    # Business settings and preferences
    brand_voice = Column(Text, nullable=True)  # Brand voice description
    brand_guidelines = Column(JSON, nullable=True)  # Colors, fonts, style guide
    keywords = Column(JSON, nullable=True)  # Primary keywords
    competitors = Column(JSON, nullable=True)  # Competitor URLs/names
    
    # Social media handles
    social_handles = Column(JSON, nullable=True)  # {"linkedin": "handle", "twitter": "handle"}
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="businesses")
    industry_ref = relationship("Industry", back_populates="businesses")
    content = relationship("Content", back_populates="business", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="business", cascade="all, delete-orphan")
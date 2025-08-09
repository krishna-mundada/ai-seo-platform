from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Industry(Base):
    __tablename__ = "industries"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    slug = Column(String, nullable=False, unique=True, index=True)  # URL-friendly version
    description = Column(Text, nullable=True)
    icon = Column(String, nullable=True)  # Icon name or emoji
    color = Column(String, nullable=True)  # Hex color for UI
    sort_order = Column(Integer, default=0)  # For custom ordering
    is_active = Column(Boolean, default=True)  # Soft delete
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    businesses = relationship("Business", back_populates="industry_ref")
    
    def __repr__(self):
        return f"<Industry(id={self.id}, name='{self.name}')>"
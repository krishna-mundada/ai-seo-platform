from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.models.content import Content, ContentType, ContentStatus
from app.repositories.base_repository import BaseRepository
from datetime import datetime

class ContentRepository(BaseRepository[Content]):
    def __init__(self, db: Session):
        super().__init__(db, Content)
    
    def get_multi(
        self, 
        business_id: Optional[int] = None,
        content_type: Optional[str] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Content]:
        """Get content with optional filters"""
        query = self.db.query(Content).options(joinedload(Content.business))
        
        if business_id:
            query = query.filter(Content.business_id == business_id)
        
        if content_type:
            query = query.filter(Content.content_type == content_type)
        
        return query.order_by(Content.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_status(self, status: ContentStatus, skip: int = 0, limit: int = 100) -> List[Content]:
        """Get content by status"""
        return (
            self.db.query(Content)
            .filter(Content.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_pending_approval(self, business_id: Optional[int] = None) -> List[Content]:
        """Get content pending approval"""
        query = self.db.query(Content).filter(Content.status == ContentStatus.PENDING_APPROVAL)
        
        if business_id:
            query = query.filter(Content.business_id == business_id)
        
        return query.all()
    
    def get_scheduled_content(self, before_date: Optional[datetime] = None) -> List[Content]:
        """Get scheduled content ready for publishing"""
        query = self.db.query(Content).filter(Content.status == ContentStatus.SCHEDULED)
        
        if before_date:
            query = query.filter(Content.scheduled_publish_at <= before_date)
        
        return query.all()
    
    def update_status(self, content_id: int, status: ContentStatus) -> Optional[Content]:
        """Update content status"""
        content = self.get_by_id(content_id)
        if content:
            content.status = status
            self.db.commit()
            self.db.refresh(content)
        return content

    def save_as_draft(self, content_id: int) -> Optional[Content]:
        """Save content as draft"""
        return self.update_status(content_id, ContentStatus.DRAFT)

    def approve_content(self, content_id: int) -> Optional[Content]:
        """Approve content for publishing"""
        return self.update_status(content_id, ContentStatus.APPROVED)
    
    def publish_content(self, content_id: int) -> Optional[Content]:
        """Mark content as published"""
        content = self.update_status(content_id, ContentStatus.PUBLISHED)
        if content:
            content.published_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(content)
        return content
    
    def update_performance_metrics(self, content_id: int, views: int = 0, clicks: int = 0, engagement_rate: int = 0) -> Optional[Content]:
        """Update content performance metrics"""
        content = self.get_by_id(content_id)
        if content:
            content.views += views
            content.clicks += clicks
            if engagement_rate > 0:
                content.engagement_rate = engagement_rate
            self.db.commit()
            self.db.refresh(content)
        return content
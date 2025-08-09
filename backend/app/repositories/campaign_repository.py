from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.campaign import Campaign, CampaignStatus, CampaignType
from app.repositories.base_repository import BaseRepository
from datetime import datetime

class CampaignRepository(BaseRepository[Campaign]):
    def __init__(self, db: Session):
        super().__init__(db, Campaign)
    
    def get_multi(
        self, 
        business_id: Optional[int] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Campaign]:
        """Get campaigns with optional business filter"""
        query = self.db.query(Campaign)
        
        if business_id:
            query = query.filter(Campaign.business_id == business_id)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_status(self, status: CampaignStatus, skip: int = 0, limit: int = 100) -> List[Campaign]:
        """Get campaigns by status"""
        return (
            self.db.query(Campaign)
            .filter(Campaign.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_active_campaigns(self, business_id: Optional[int] = None) -> List[Campaign]:
        """Get active campaigns"""
        query = self.db.query(Campaign).filter(Campaign.status == CampaignStatus.ACTIVE)
        
        if business_id:
            query = query.filter(Campaign.business_id == business_id)
        
        return query.all()
    
    def get_campaigns_by_type(self, campaign_type: CampaignType, skip: int = 0, limit: int = 100) -> List[Campaign]:
        """Get campaigns by type"""
        return (
            self.db.query(Campaign)
            .filter(Campaign.campaign_type == campaign_type)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def start_campaign(self, campaign_id: int) -> Optional[Campaign]:
        """Start a campaign (set status to active)"""
        campaign = self.get_by_id(campaign_id)
        if campaign:
            campaign.status = CampaignStatus.ACTIVE
            if not campaign.start_date:
                campaign.start_date = datetime.utcnow()
            self.db.commit()
            self.db.refresh(campaign)
        return campaign
    
    def pause_campaign(self, campaign_id: int) -> Optional[Campaign]:
        """Pause a campaign"""
        campaign = self.get_by_id(campaign_id)
        if campaign:
            campaign.status = CampaignStatus.PAUSED
            self.db.commit()
            self.db.refresh(campaign)
        return campaign
    
    def complete_campaign(self, campaign_id: int) -> Optional[Campaign]:
        """Mark campaign as completed"""
        campaign = self.get_by_id(campaign_id)
        if campaign:
            campaign.status = CampaignStatus.COMPLETED
            campaign.end_date = datetime.utcnow()
            self.db.commit()
            self.db.refresh(campaign)
        return campaign
    
    def update_campaign_metrics(self, campaign_id: int, content_pieces: int = 0, published: int = 0, views: int = 0, clicks: int = 0) -> Optional[Campaign]:
        """Update campaign performance metrics"""
        campaign = self.get_by_id(campaign_id)
        if campaign:
            campaign.total_content_pieces += content_pieces
            campaign.published_content += published
            campaign.total_views += views
            campaign.total_clicks += clicks
            
            # Calculate average engagement rate
            if campaign.total_views > 0:
                campaign.avg_engagement_rate = int((campaign.total_clicks / campaign.total_views) * 100 * 100)
            
            self.db.commit()
            self.db.refresh(campaign)
        return campaign
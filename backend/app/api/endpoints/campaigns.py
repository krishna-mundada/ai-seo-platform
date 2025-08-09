from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse
from app.repositories.campaign_repository import CampaignRepository

router = APIRouter()

@router.post("/", response_model=CampaignResponse)
async def create_campaign(
    campaign_data: CampaignCreate,
    db: Session = Depends(get_db)
):
    """Create a new marketing campaign"""
    repo = CampaignRepository(db)
    campaign = repo.create(campaign_data.dict())
    return campaign

@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db)
):
    """Get campaign by ID"""
    repo = CampaignRepository(db)
    campaign = repo.get_by_id(campaign_id)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    return campaign

@router.get("/", response_model=List[CampaignResponse])
async def list_campaigns(
    business_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List campaigns"""
    repo = CampaignRepository(db)
    campaigns = repo.get_multi(business_id=business_id, skip=skip, limit=limit)
    return campaigns

@router.put("/{campaign_id}/start")
async def start_campaign(
    campaign_id: int,
    db: Session = Depends(get_db)
):
    """Start a campaign (activate AI content generation)"""
    repo = CampaignRepository(db)
    campaign = repo.start_campaign(campaign_id)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    return {"message": "Campaign started", "campaign_id": campaign_id}
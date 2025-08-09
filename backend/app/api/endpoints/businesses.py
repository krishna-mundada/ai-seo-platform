from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.business import BusinessCreate, BusinessUpdate, BusinessResponse
from app.repositories.business_repository import BusinessRepository

router = APIRouter()

@router.post("/", response_model=BusinessResponse)
async def create_business(
    business_data: BusinessCreate,
    db: Session = Depends(get_db)
):
    """Create a new business profile"""
    repo = BusinessRepository(db)
    business = repo.create(business_data.dict())
    return business

@router.get("/{business_id}", response_model=BusinessResponse)
async def get_business(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Get business by ID"""
    repo = BusinessRepository(db)
    business = repo.get_by_id(business_id)
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    return business

@router.put("/{business_id}", response_model=BusinessResponse)
async def update_business(
    business_id: int,
    business_update: BusinessUpdate,
    db: Session = Depends(get_db)
):
    """Update business profile"""
    repo = BusinessRepository(db)
    business = repo.update(business_id, business_update.dict(exclude_unset=True))
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    return business

@router.get("/", response_model=List[BusinessResponse])
async def list_businesses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all businesses (for development - add auth later)"""
    repo = BusinessRepository(db)
    businesses = repo.get_multi(skip=skip, limit=limit)
    return businesses

@router.delete("/{business_id}")
async def delete_business(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Delete business and all associated content (CASCADE)"""
    repo = BusinessRepository(db)
    business = repo.get_by_id(business_id)
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    # Check content count for informative message
    from app.models.content import Content
    content_count = db.query(Content).filter(Content.business_id == business_id).count()
    
    # Database CASCADE will handle associated content deletion automatically
    success = repo.delete(business_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete business"
        )
    
    message = f"Business deleted successfully"
    if content_count > 0:
        message += f" (along with {content_count} associated content pieces)"
        
    return {"message": message, "business_id": business_id}
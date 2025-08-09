from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.industry import (
    IndustryCreate, 
    IndustryUpdate, 
    IndustryResponse, 
    IndustryListResponse
)
from app.repositories.industry_repository import IndustryRepository

router = APIRouter()

@router.get("/", response_model=List[IndustryListResponse])
async def list_industries(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List industries with business counts"""
    repo = IndustryRepository(db)
    
    if search:
        industries = repo.search_by_name(search, skip=skip, limit=limit)
        # Convert to list response format
        return [
            IndustryListResponse(
                id=industry.id,
                name=industry.name,
                slug=industry.slug,
                icon=industry.icon,
                color=industry.color,
                is_active=industry.is_active,
                business_count=0  # Would need separate query for search results
            )
            for industry in industries
        ]
    
    industries_with_counts = repo.get_industries_with_counts(
        skip=skip, 
        limit=limit, 
        active_only=active_only
    )
    
    return [
        IndustryListResponse(
            id=row.id,
            name=row.name,
            slug=row.slug,
            icon=row.icon,
            color=row.color,
            is_active=row.is_active,
            business_count=row.business_count
        )
        for row in industries_with_counts
    ]

@router.get("/{industry_id}", response_model=IndustryResponse)
async def get_industry(
    industry_id: int,
    db: Session = Depends(get_db)
):
    """Get industry by ID with business count"""
    repo = IndustryRepository(db)
    industry = repo.get_with_business_count(industry_id)
    if not industry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Industry not found"
        )
    return industry

@router.get("/slug/{slug}", response_model=IndustryResponse)
async def get_industry_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get industry by slug"""
    repo = IndustryRepository(db)
    industry = repo.get_by_slug(slug)
    if not industry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Industry not found"
        )
    
    # Add business count
    industry = repo.get_with_business_count(industry.id)
    return industry

@router.post("/", response_model=IndustryResponse)
async def create_industry(
    industry_data: IndustryCreate,
    db: Session = Depends(get_db)
):
    """Create a new industry"""
    repo = IndustryRepository(db)
    
    # Check if slug already exists
    existing = repo.get_by_slug(industry_data.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Industry with this slug already exists"
        )
    
    industry = repo.create(industry_data.model_dump())
    return repo.get_with_business_count(industry.id)

@router.put("/{industry_id}", response_model=IndustryResponse)
async def update_industry(
    industry_id: int,
    industry_update: IndustryUpdate,
    db: Session = Depends(get_db)
):
    """Update an industry"""
    repo = IndustryRepository(db)
    
    # Check if slug conflicts (if being updated)
    if industry_update.name:
        # Auto-generate slug from name if not provided
        update_data = industry_update.model_dump(exclude_unset=True)
        if 'slug' not in update_data:
            update_data['slug'] = industry_update.name.lower().replace(' ', '-').replace('&', 'and')
    
    industry = repo.update(industry_id, industry_update.model_dump(exclude_unset=True))
    if not industry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Industry not found"
        )
    return repo.get_with_business_count(industry.id)

@router.delete("/{industry_id}")
async def delete_industry(
    industry_id: int,
    force: bool = Query(False, description="Force delete even if businesses exist"),
    db: Session = Depends(get_db)
):
    """Delete or deactivate an industry"""
    repo = IndustryRepository(db)
    industry = repo.get_with_business_count(industry_id)
    
    if not industry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Industry not found"
        )
    
    # Check if industry has businesses
    if hasattr(industry, 'business_count') and industry.business_count > 0:
        if not force:
            # Soft delete (deactivate) instead of hard delete
            success = repo.deactivate(industry_id)
            if success:
                return {
                    "message": f"Industry deactivated (had {industry.business_count} businesses)",
                    "industry_id": industry_id,
                    "deactivated": True
                }
        else:
            # Force delete - this might cause issues with existing businesses
            success = repo.delete(industry_id)
            if success:
                return {
                    "message": f"Industry force deleted (had {industry.business_count} businesses)",
                    "industry_id": industry_id,
                    "deleted": True
                }
    else:
        # Safe to hard delete
        success = repo.delete(industry_id)
        if success:
            return {
                "message": "Industry deleted successfully",
                "industry_id": industry_id,
                "deleted": True
            }
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to delete industry"
    )

@router.put("/{industry_id}/activate")
async def activate_industry(
    industry_id: int,
    db: Session = Depends(get_db)
):
    """Activate a deactivated industry"""
    repo = IndustryRepository(db)
    success = repo.activate(industry_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Industry not found"
        )
    return {"message": "Industry activated successfully", "industry_id": industry_id}
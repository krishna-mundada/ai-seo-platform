from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.content import ContentCreate, ContentResponse, ContentGenerate, ContentUpdate
from app.repositories.content_repository import ContentRepository
from app.services.ai_content_service import AIContentService

router = APIRouter()

@router.post("/generate", response_model=ContentResponse)
async def generate_content(
    content_request: ContentGenerate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate AI content for a business"""
    # Get business info for context
    from app.repositories.business_repository import BusinessRepository
    business_repo = BusinessRepository(db)
    business = business_repo.get_by_id(content_request.business_id)
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    # Generate content using AI service
    ai_service = AIContentService()
    content_data = await ai_service.generate_content(
        business=business,
        content_type=content_request.content_type,
        topic=content_request.topic,
        keywords=content_request.keywords
    )
    
    # Save to database
    content_repo = ContentRepository(db)
    content = content_repo.create(content_data)
    
    return content

@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: int,
    db: Session = Depends(get_db)
):
    """Get content by ID"""
    repo = ContentRepository(db)
    content = repo.get_by_id(content_id)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    return content

@router.get("/", response_model=List[ContentResponse])
async def list_content(
    business_id: Optional[int] = None,
    content_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List content with optional filters"""
    repo = ContentRepository(db)
    content = repo.get_multi(
        business_id=business_id,
        content_type=content_type,
        skip=skip,
        limit=limit
    )
    return content

@router.post("/", response_model=ContentResponse)
async def create_content(
    content_data: ContentCreate,
    db: Session = Depends(get_db)
):
    """Create new content"""
    repo = ContentRepository(db)
    content = repo.create(content_data.model_dump())
    return content

@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: int,
    content_update: ContentUpdate,
    db: Session = Depends(get_db)
):
    """Update content"""
    repo = ContentRepository(db)
    content = repo.update(content_id, content_update.model_dump(exclude_unset=True))
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    return content

@router.delete("/{content_id}")
async def delete_content(
    content_id: int,
    db: Session = Depends(get_db)
):
    """Delete content"""
    repo = ContentRepository(db)
    content = repo.get_by_id(content_id)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    success = repo.delete(content_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete content"
        )
        
    return {"message": "Content deleted successfully", "content_id": content_id}

@router.put("/{content_id}/draft")
async def save_as_draft(
    content_id: int,
    db: Session = Depends(get_db)
):
    """Save content as draft"""
    repo = ContentRepository(db)
    content = repo.save_as_draft(content_id)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    return {"message": "Content saved as draft", "content_id": content_id}

@router.put("/{content_id}/approve")
async def approve_content(
    content_id: int,
    db: Session = Depends(get_db)
):
    """Approve content for publishing"""
    repo = ContentRepository(db)
    content = repo.approve_content(content_id)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    return {"message": "Content approved", "content_id": content_id}

@router.put("/{content_id}/publish")
async def publish_content(
    content_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Publish content to platforms"""
    # This will be implemented later with platform integrations
    return {"message": "Publishing feature coming soon", "content_id": content_id}
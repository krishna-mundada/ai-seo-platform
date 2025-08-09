from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.suggestions import TopicSuggestionsRequest, KeywordSuggestionsRequest, TopicSuggestionsResponse, KeywordSuggestionsResponse
from app.services.ai_content_service import AIContentService
from app.repositories.business_repository import BusinessRepository

router = APIRouter()

@router.post("/topics", response_model=TopicSuggestionsResponse)
async def generate_topic_suggestions(
    request: TopicSuggestionsRequest,
    db: Session = Depends(get_db)
):
    """Generate AI-powered topic suggestions"""
    # Get business info for context
    business_repo = BusinessRepository(db)
    business = business_repo.get_by_id(request.business_id)
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    # Generate suggestions using AI service
    ai_service = AIContentService()
    suggestions = await ai_service.generate_topic_suggestions(
        business=business,
        content_type=request.content_type,
        category=request.category,
        description=request.description
    )
    
    return TopicSuggestionsResponse(suggestions=suggestions)

@router.post("/keywords", response_model=KeywordSuggestionsResponse)
async def generate_keyword_suggestions(
    request: KeywordSuggestionsRequest,
    db: Session = Depends(get_db)
):
    """Generate AI-powered keyword suggestions"""
    # Get business info for context
    business_repo = BusinessRepository(db)
    business = business_repo.get_by_id(request.business_id)
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    # Generate suggestions using AI service
    ai_service = AIContentService()
    suggestions = await ai_service.generate_keyword_suggestions(
        business=business,
        content_type=request.content_type,
        category=request.category,
        topic=request.topic,
        description=request.description
    )
    
    return KeywordSuggestionsResponse(suggestions=suggestions)
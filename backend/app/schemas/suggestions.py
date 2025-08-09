from pydantic import BaseModel, Field
from typing import List, Optional

class TopicSuggestionsRequest(BaseModel):
    business_id: int = Field(..., description="ID of the business")
    content_type: str = Field(..., description="Type of content (blog_post, linkedin_post, etc.)")
    category: Optional[str] = Field(None, description="Content category (educational, promotional, etc.)")
    description: Optional[str] = Field(None, description="Additional context for topic generation")

class TopicSuggestionsResponse(BaseModel):
    suggestions: List[str] = Field(..., description="List of AI-generated topic suggestions")

class KeywordSuggestionsRequest(BaseModel):
    business_id: int = Field(..., description="ID of the business")
    content_type: str = Field(..., description="Type of content (blog_post, linkedin_post, etc.)")
    category: Optional[str] = Field(None, description="Content category (educational, promotional, etc.)")
    topic: Optional[str] = Field(None, description="Content topic for keyword context")
    description: Optional[str] = Field(None, description="Additional context for keyword generation")

class KeywordSuggestionsResponse(BaseModel):
    suggestions: List[str] = Field(..., description="List of AI-generated keyword suggestions")
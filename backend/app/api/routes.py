from fastapi import APIRouter
from app.api.endpoints import users, businesses, industries, content, campaigns, suggestions

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(businesses.router, prefix="/businesses", tags=["businesses"])
api_router.include_router(industries.router, prefix="/industries", tags=["industries"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(suggestions.router, prefix="/suggestions", tags=["suggestions"])
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.business import Business
from app.repositories.base_repository import BaseRepository

class BusinessRepository(BaseRepository[Business]):
    def __init__(self, db: Session):
        super().__init__(db, Business)
    
    def get_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Business]:
        """Get businesses owned by a user"""
        return (
            self.db.query(Business)
            .filter(Business.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_industry(self, industry: str, skip: int = 0, limit: int = 100) -> List[Business]:
        """Get businesses by industry"""
        return (
            self.db.query(Business)
            .filter(Business.industry.ilike(f"%{industry}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[Business]:
        """Search businesses by name"""
        return (
            self.db.query(Business)
            .filter(Business.name.ilike(f"%{name}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )
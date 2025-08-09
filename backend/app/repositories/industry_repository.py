from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.models.industry import Industry
from app.models.business import Business
from app.repositories.base_repository import BaseRepository

class IndustryRepository(BaseRepository[Industry]):
    def __init__(self, db: Session):
        super().__init__(db, Industry)
    
    def get_active_industries(self, skip: int = 0, limit: int = 100) -> List[Industry]:
        """Get all active industries"""
        return (
            self.db.query(Industry)
            .filter(Industry.is_active == True)
            .order_by(Industry.sort_order.asc(), Industry.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_slug(self, slug: str) -> Optional[Industry]:
        """Get industry by slug"""
        return self.db.query(Industry).filter(Industry.slug == slug).first()
    
    def get_with_business_count(self, industry_id: int) -> Optional[Industry]:
        """Get industry with business count"""
        industry = self.get_by_id(industry_id)
        if industry:
            business_count = (
                self.db.query(func.count(Business.id))
                .filter(Business.industry_id == industry_id)
                .scalar()
            )
            # Add business_count as a dynamic attribute
            industry.business_count = business_count or 0
        return industry
    
    def get_industries_with_counts(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Industry]:
        """Get industries with business counts"""
        query = (
            self.db.query(
                Industry.id,
                Industry.name,
                Industry.slug,
                Industry.description,
                Industry.icon,
                Industry.color,
                Industry.sort_order,
                Industry.is_active,
                Industry.created_at,
                Industry.updated_at,
                func.count(Business.id).label('business_count')
            )
            .outerjoin(Business, Industry.id == Business.industry_id)
            .group_by(Industry.id)
            .order_by(Industry.sort_order.asc(), Industry.name.asc())
        )
        
        if active_only:
            query = query.filter(Industry.is_active == True)
            
        return query.offset(skip).limit(limit).all()
    
    def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[Industry]:
        """Search industries by name"""
        return (
            self.db.query(Industry)
            .filter(Industry.name.ilike(f"%{name}%"))
            .filter(Industry.is_active == True)
            .order_by(Industry.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def deactivate(self, industry_id: int) -> bool:
        """Soft delete an industry by marking as inactive"""
        industry = self.get_by_id(industry_id)
        if industry:
            industry.is_active = False
            self.db.commit()
            return True
        return False
    
    def activate(self, industry_id: int) -> bool:
        """Reactivate an industry"""
        industry = self.get_by_id(industry_id)
        if industry:
            industry.is_active = True
            self.db.commit()
            return True
        return False
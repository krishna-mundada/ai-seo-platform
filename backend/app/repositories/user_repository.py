from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from app.models.user import User
from app.repositories.base_repository import BaseRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)
    
    def create(self, obj_data: Dict[str, Any]) -> User:
        """Create user with hashed password"""
        if "password" in obj_data:
            obj_data["hashed_password"] = pwd_context.hash(obj_data.pop("password"))
        return super().create(obj_data)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = self.get_by_email(email)
        if user and self.verify_password(password, user.hashed_password):
            return user
        return None
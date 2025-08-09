import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.content import Content


class TestBusinessCascadeDelete:
    """Test suite for CASCADE delete functionality"""

    def test_delete_business_with_no_content(self, client: TestClient, created_business):
        """Test deleting a business with no associated content"""
        business_id = created_business.id
        
        # Delete the business
        response = client.delete(f"/api/v1/businesses/{business_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Business deleted successfully"
        assert data["business_id"] == business_id
        
        # Verify business is deleted
        get_response = client.get(f"/api/v1/businesses/{business_id}")
        assert get_response.status_code == 404

    def test_delete_business_with_single_content(self, client: TestClient, created_content):
        """Test deleting a business with one piece of content"""
        business = created_content.business
        business_id = business.id
        content_id = created_content.id
        
        # Verify content exists before deletion
        content_response = client.get(f"/api/v1/content/{content_id}")
        assert content_response.status_code == 200
        
        # Delete the business
        response = client.delete(f"/api/v1/businesses/{business_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert "Business deleted successfully" in data["message"]
        assert "1 associated content pieces" in data["message"]
        assert data["business_id"] == business_id
        
        # Verify business is deleted
        get_business_response = client.get(f"/api/v1/businesses/{business_id}")
        assert get_business_response.status_code == 404
        
        # Verify content is also deleted (CASCADE)
        get_content_response = client.get(f"/api/v1/content/{content_id}")
        assert get_content_response.status_code == 404

    def test_delete_business_with_multiple_content(self, client: TestClient, created_business, db_session: Session):
        """Test deleting a business with multiple pieces of content"""
        business_id = created_business.id
        
        # Create multiple content pieces
        from app.models.content import ContentType, ContentStatus
        content_pieces = []
        for i in range(5):
            content_data = {
                "title": f"Test Content {i+1}",
                "content_text": f"This is test content piece number {i+1}",
                "content_type": ContentType.BLOG_POST,
                "status": ContentStatus.DRAFT,
                "business_id": business_id
            }
            content = Content(**content_data)
            db_session.add(content)
            content_pieces.append(content)
        
        db_session.commit()
        for content in content_pieces:
            db_session.refresh(content)
        
        # Verify all content exists
        for content in content_pieces:
            response = client.get(f"/api/v1/content/{content.id}")
            assert response.status_code == 200
        
        # Delete the business
        response = client.delete(f"/api/v1/businesses/{business_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert "Business deleted successfully" in data["message"]
        assert "5 associated content pieces" in data["message"]
        assert data["business_id"] == business_id
        
        # Verify business is deleted
        get_business_response = client.get(f"/api/v1/businesses/{business_id}")
        assert get_business_response.status_code == 404
        
        # Verify all content pieces are deleted (CASCADE)
        for content in content_pieces:
            get_content_response = client.get(f"/api/v1/content/{content.id}")
            assert get_content_response.status_code == 404

    def test_delete_nonexistent_business(self, client: TestClient):
        """Test deleting a business that doesn't exist"""
        response = client.delete("/api/v1/businesses/999999")
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Business not found"

    def test_cascade_delete_preserves_other_businesses_content(self, client: TestClient, db_session: Session, created_user):
        """Test that CASCADE delete only affects the specific business and its content"""
        # Create two businesses
        business1_data = {
            "name": "Business 1",
            "industry": "Technology",
            "description": "First business",
            "owner_id": created_user.id
        }
        business2_data = {
            "name": "Business 2", 
            "industry": "Marketing",
            "description": "Second business",
            "owner_id": created_user.id
        }
        
        business1 = Business(**business1_data)
        business2 = Business(**business2_data)
        db_session.add(business1)
        db_session.add(business2)
        db_session.commit()
        db_session.refresh(business1)
        db_session.refresh(business2)
        
        # Create content for both businesses
        from app.models.content import ContentType
        content1_data = {
            "title": "Business 1 Content",
            "content_text": "Content for business 1",
            "content_type": ContentType.BLOG_POST,
            "business_id": business1.id
        }
        content2_data = {
            "title": "Business 2 Content",
            "content_text": "Content for business 2", 
            "content_type": ContentType.BLOG_POST,
            "business_id": business2.id
        }
        
        content1 = Content(**content1_data)
        content2 = Content(**content2_data)
        db_session.add(content1)
        db_session.add(content2)
        db_session.commit()
        db_session.refresh(content1)
        db_session.refresh(content2)
        
        # Delete business1
        response = client.delete(f"/api/v1/businesses/{business1.id}")
        assert response.status_code == 200
        
        # Verify business1 and its content are deleted
        get_business1_response = client.get(f"/api/v1/businesses/{business1.id}")
        assert get_business1_response.status_code == 404
        
        get_content1_response = client.get(f"/api/v1/content/{content1.id}")
        assert get_content1_response.status_code == 404
        
        # Verify business2 and its content still exist
        get_business2_response = client.get(f"/api/v1/businesses/{business2.id}")
        assert get_business2_response.status_code == 200
        
        get_content2_response = client.get(f"/api/v1/content/{content2.id}")
        assert get_content2_response.status_code == 200

    def test_delete_business_database_consistency(self, client: TestClient, created_content, db_session: Session):
        """Test that CASCADE delete maintains database consistency"""
        business = created_content.business
        business_id = business.id
        content_id = created_content.id
        
        # Count total records before deletion
        business_count_before = db_session.query(Business).count()
        content_count_before = db_session.query(Content).count()
        
        assert business_count_before >= 1
        assert content_count_before >= 1
        
        # Delete the business
        response = client.delete(f"/api/v1/businesses/{business_id}")
        assert response.status_code == 200
        
        # Refresh session to get updated counts
        db_session.expire_all()
        
        # Verify counts decreased by exactly the expected amount
        business_count_after = db_session.query(Business).count()
        content_count_after = db_session.query(Content).count()
        
        assert business_count_after == business_count_before - 1
        assert content_count_after == content_count_before - 1
        
        # Verify specific records are gone
        business_exists = db_session.query(Business).filter(Business.id == business_id).first()
        content_exists = db_session.query(Content).filter(Content.id == content_id).first()
        
        assert business_exists is None
        assert content_exists is None
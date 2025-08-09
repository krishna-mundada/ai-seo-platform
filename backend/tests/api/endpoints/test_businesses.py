import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.business import Business


class TestBusinessCRUD:
    """Test suite for Business CRUD operations"""

    def test_create_business(self, client: TestClient, created_user, sample_business_data):
        """Test creating a new business"""
        response = client.post("/api/v1/businesses/", json=sample_business_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_business_data["name"]
        assert data["industry"] == sample_business_data["industry"]
        assert data["description"] == sample_business_data["description"]
        assert data["website_url"] == sample_business_data["website_url"]
        assert data["target_audience"] == sample_business_data["target_audience"]
        assert data["brand_voice"] == sample_business_data["brand_voice"]
        assert data["owner_id"] == sample_business_data["owner_id"]
        assert "id" in data
        assert "created_at" in data

    def test_create_business_missing_required_fields(self, client: TestClient):
        """Test creating business with missing required fields"""
        incomplete_data = {
            "industry": "Technology",
            "description": "Missing name field"
        }
        
        response = client.post("/api/v1/businesses/", json=incomplete_data)
        assert response.status_code == 422  # Validation error

    def test_get_business_by_id(self, client: TestClient, created_business):
        """Test retrieving a business by ID"""
        business_id = created_business.id
        
        response = client.get(f"/api/v1/businesses/{business_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == business_id
        assert data["name"] == created_business.name
        assert data["industry"] == created_business.industry

    def test_get_nonexistent_business(self, client: TestClient):
        """Test retrieving a business that doesn't exist"""
        response = client.get("/api/v1/businesses/999999")
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Business not found"

    def test_list_businesses_empty(self, client: TestClient):
        """Test listing businesses when none exist"""
        response = client.get("/api/v1/businesses/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_list_businesses_with_data(self, client: TestClient, created_business):
        """Test listing businesses when data exists"""
        response = client.get("/api/v1/businesses/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Check that our created business is in the list
        business_ids = [business["id"] for business in data]
        assert created_business.id in business_ids

    def test_list_businesses_pagination(self, client: TestClient, db_session: Session, created_user):
        """Test business listing pagination"""
        # Create multiple businesses
        businesses = []
        for i in range(5):
            business_data = {
                "name": f"Business {i+1}",
                "industry": "Technology",
                "description": f"Test business number {i+1}",
                "owner_id": created_user.id
            }
            business = Business(**business_data)
            db_session.add(business)
            businesses.append(business)
        
        db_session.commit()
        
        # Test pagination
        response = client.get("/api/v1/businesses/?skip=0&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        
        response = client.get("/api/v1/businesses/?skip=3&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2  # Remaining businesses

    def test_update_business(self, client: TestClient, created_business):
        """Test updating a business"""
        business_id = created_business.id
        update_data = {
            "name": "Updated Business Name",
            "description": "Updated description",
            "brand_voice": "Updated brand voice"
        }
        
        response = client.put(f"/api/v1/businesses/{business_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"] 
        assert data["brand_voice"] == update_data["brand_voice"]
        assert data["industry"] == created_business.industry  # Unchanged field

    def test_update_nonexistent_business(self, client: TestClient):
        """Test updating a business that doesn't exist"""
        update_data = {"name": "Updated Name"}
        
        response = client.put("/api/v1/businesses/999999", json=update_data)
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Business not found"

    def test_partial_update_business(self, client: TestClient, created_business):
        """Test partial update of business (only some fields)"""
        business_id = created_business.id
        original_name = created_business.name
        
        update_data = {"description": "Only updating description"}
        
        response = client.put(f"/api/v1/businesses/{business_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == update_data["description"]
        assert data["name"] == original_name  # Should remain unchanged

    def test_delete_business_basic(self, client: TestClient, created_business):
        """Test basic business deletion (covered more thoroughly in cascade tests)"""
        business_id = created_business.id
        
        response = client.delete(f"/api/v1/businesses/{business_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert "Business deleted successfully" in data["message"]
        assert data["business_id"] == business_id
        
        # Verify deletion
        get_response = client.get(f"/api/v1/businesses/{business_id}")
        assert get_response.status_code == 404
# AI SEO Platform - Test Suite

Comprehensive automated testing for the AI SEO Platform backend, replacing manual curl commands with reliable, repeatable tests.

## Quick Start

```bash
# Run all tests
python test_runner.py --all

# Run specific test suites
python test_runner.py --cascade    # CASCADE delete tests
python test_runner.py --business   # Business API tests  
python test_runner.py --content    # Content API tests

# Run with coverage report
python test_runner.py --all --coverage
```

## Test Suites

### 1. CASCADE Delete Tests (`test_business_cascade_delete.py`)
Tests the database CASCADE delete functionality that automatically removes associated content when a business is deleted.

**Key Tests:**
- ✅ Delete business with no content
- ✅ Delete business with single content piece  
- ✅ Delete business with multiple content pieces
- ✅ Verify other businesses' content is preserved
- ✅ Database consistency checks
- ✅ Non-existent business handling

### 2. Business API Tests (`test_businesses.py`) 
Full CRUD testing for the Business management endpoints.

**Key Tests:**
- ✅ Create business with validation
- ✅ Get business by ID
- ✅ List businesses with pagination
- ✅ Update business (full and partial)
- ✅ Delete business
- ✅ Error handling for non-existent resources

### 3. Content API Tests (`test_content.py`)
Complete testing for Content management and its relationship with businesses.

**Key Tests:**
- ✅ Create content with business association
- ✅ Get content by ID
- ✅ List and filter content by business
- ✅ Update content including status changes
- ✅ Delete individual content
- ✅ Business-content relationship verification

## Test Infrastructure

### Database
- Uses **SQLite in-memory database** for fast, isolated tests
- **Fresh database** for each test to prevent interference
- **Auto-creation/cleanup** of tables and data

### Fixtures
- `created_user` - Test user with proper authentication fields
- `created_business` - Business associated with test user
- `created_content` - Content associated with test business
- `sample_*_data` - Template data for creating test objects

### Test Client
- **FastAPI TestClient** for API endpoint testing
- **Dependency injection** override for database session
- **Automatic JSON serialization** with enum handling

## Coverage

Run with coverage to see test coverage:
```bash
python test_runner.py --all --coverage
# View HTML report at htmlcov/index.html
```

## Key Testing Features

### CASCADE Delete Verification
```python
# Verify business deletion removes all associated content
response = client.delete(f"/api/v1/businesses/{business_id}")
assert "5 associated content pieces" in response.json()["message"]

# Verify all content is actually deleted from database
assert db_session.query(Content).filter(Content.business_id == business_id).count() == 0
```

### Enum Handling
```python
# Tests handle SQLAlchemy enum types properly
content_data["content_type"] = ContentType.BLOG_POST  # For database
api_data["content_type"] = "blog_post"  # For API calls
```

### Error Scenarios
```python
# Test non-existent resource handling
response = client.get("/api/v1/businesses/999999")
assert response.status_code == 404
assert response.json()["detail"] == "Business not found"
```

## Running Tests in CI/CD

The test suite is designed to be CI/CD friendly:

- **Fast execution** (< 1 second total)
- **No external dependencies** (uses in-memory SQLite)
- **Deterministic results** (fresh database per test)
- **Clear pass/fail reporting** 
- **Coverage reporting** available

## Test Data

Sample test data is realistic and consistent:

```python
# Business
{
    "name": "Test Business Inc",
    "industry": "Technology", 
    "description": "A test business for automated testing",
    "website_url": "https://testbusiness.com",
    "target_audience": "Small and medium businesses",
    "brand_voice": "Professional and innovative"
}

# Content  
{
    "title": "Test Blog Post",
    "content_text": "This is a test blog post content...",
    "content_type": "blog_post",
    "status": "draft"
}
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install dependencies
   ```bash
   pip install pytest pytest-asyncio pytest-cov httpx ollama openai anthropic
   ```

2. **Database errors**: Tests use fresh SQLite database - no setup needed

3. **API endpoint 405 errors**: Ensure API container is running
   ```bash
   docker restart ai_seo_api
   ```

### Test Debugging

Run individual tests with verbose output:
```bash
python -m pytest tests/api/endpoints/test_business_cascade_delete.py::TestBusinessCascadeDelete::test_delete_business_with_multiple_content -v
```

## Future Enhancements

- [ ] Performance tests for large datasets
- [ ] Integration tests with real AI services
- [ ] End-to-end tests with frontend
- [ ] Load testing for concurrent users
- [ ] Security testing for authentication
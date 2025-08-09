import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db
from app.models import business, content, user
from app.core.config import settings

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    """Create test database engine"""
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(db_engine):
    """Create a fresh database session for each test"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    """Create test client with dependency override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_user_data():
    """Sample user data for tests"""
    return {
        "id": 1,
        "email": "test@example.com",
        "hashed_password": "fake_hashed_password",
        "first_name": "Test",
        "last_name": "User"
    }

@pytest.fixture
def sample_business_data():
    """Sample business data for tests"""
    return {
        "name": "Test Business Inc",
        "industry": "Technology",
        "description": "A test business for automated testing",
        "website_url": "https://testbusiness.com",
        "target_audience": "Small and medium businesses",
        "brand_voice": "Professional and innovative",
        "owner_id": 1
    }

@pytest.fixture
def sample_content_data():
    """Sample content data for tests"""
    from app.models.content import ContentType, ContentStatus
    return {
        "title": "Test Blog Post",
        "content_text": "This is a test blog post content for CASCADE delete testing.",
        "content_type": ContentType.BLOG_POST,
        "status": ContentStatus.DRAFT,
        "meta_description": "Test meta description",
        "keywords": ["test", "automation", "pytest"],
        "ai_prompt_used": "Test prompt",
        "ai_model_used": "test-model"
    }

@pytest.fixture
def created_user(db_session, sample_user_data):
    """Create a test user in the database"""
    from app.models.user import User
    user = User(**sample_user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def created_business(db_session, created_user, sample_business_data):
    """Create a test business in the database"""
    from app.models.business import Business
    business = Business(**sample_business_data)
    db_session.add(business)
    db_session.commit()
    db_session.refresh(business)
    return business

@pytest.fixture
def created_content(db_session, created_business, sample_content_data):
    """Create test content in the database"""
    from app.models.content import Content
    content_data = {**sample_content_data, "business_id": created_business.id}
    content = Content(**content_data)
    db_session.add(content)
    db_session.commit()
    db_session.refresh(content)
    return content
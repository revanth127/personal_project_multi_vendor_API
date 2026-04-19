# FIXED: app/tests/conftest.py

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.main import app
from app.database import Base, get_db


# ============================================================================
# SESSION-LEVEL SETUP - Environment Variables & Database
# ============================================================================

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Set up test environment variables before any tests run.
    This runs once per test session.
    """
    # Set required environment variables
    os.environ["SECRET_KEY"] = "test-secret-key-do-not-use-in-production"
    os.environ["ALGORITHM"] = "HS256"
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
    
    # Use SQLite in-memory database for tests
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    
    yield
    
    # Cleanup (optional for in-memory DB)


# ============================================================================
# FUNCTION-LEVEL FIXTURES - Database & Client
# ============================================================================

@pytest.fixture
def db_engine():
    """Create test database engine with in-memory SQLite"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine):
    """Provide database session for a single test"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    db = SessionLocal()
    
    yield db
    
    db.close()


@pytest.fixture
def client(db_session):
    """
    Provide FastAPI test client with overridden database dependency.
    This ensures tests use the test database instead of production database.
    """
    def override_get_db():
        """Override the get_db dependency to use test database"""
        yield db_session
    
    # Override the dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client
    test_client = TestClient(app)
    
    yield test_client
    
    # Clear overrides after test
    app.dependency_overrides.clear()


# ============================================================================
# TEST DATA FIXTURES
# ============================================================================

@pytest.fixture
def test_user_data():
    """Fixture for buyer user test data"""
    return {
        "email": "buyer@example.com",
        "password": "securepassword123", 
        "role": "buyer"
    }


@pytest.fixture
def test_seller_data():
    """Fixture for seller user test data"""
    return {
        "email": "seller@example.com",
        "password": "securepassword123",  
        "role": "seller"
    }


@pytest.fixture
def test_user_seller():
    """Alias for seller user fixture - used by some tests"""
    return {
        "email": "seller@example.com",
        "password": "securepassword123",  
        "role": "seller"
    }


@pytest.fixture
def test_product_data():
    """Fixture for product test data"""
    return {
        "name": "Test Product",
        "description": "Test description",
        "price": 100.0, 
        "stock": 10,
        "category": "electronics"
    }


# ============================================================================
# HELPER FUNCTIONS - Authentication
# ============================================================================

def get_auth_headers(client: TestClient, user_data: dict) -> dict:
    """
    Helper function to get authentication headers for a user.
    
    This function:
    1. Registers a user if not already registered
    2. Logs in the user
    3. Returns authorization headers with the JWT token
    
    Args:
        client: TestClient instance
        user_data: Dictionary with email, password, role
        
    Returns:
        Dictionary with Authorization header containing Bearer token
    """
    # Register user
    reg_response = client.post("/api/v1/users/register", json=user_data)
    
    # Login user
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )
    
    # Extract token
    if login_response.status_code == 200:
        token = login_response.json().get("access_token")
        return {"Authorization": f"Bearer {token}"}
    else:
        # Return empty headers if login fails
        print(f"Login failed: {login_response.status_code} - {login_response.text}")
        return {}


# ============================================================================
# OPTIONAL: Debugging Fixtures
# ============================================================================

@pytest.fixture
def print_test_info():
    """
    Optional fixture for debugging - prints test info.
    
    Usage: def test_something(client, print_test_info):
    """
    import sys
    
    def _print(msg: str):
        print(f"\n{'='*60}")
        print(f"TEST INFO: {msg}")
        print(f"{'='*60}\n", file=sys.stderr)
    
    return _print

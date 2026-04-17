import pytest
<<<<<<< HEAD

@pytest.fixture
def test_user_seller(client):
    return {
        "email": "tester_new@gmail.com",
        "password": "securepassword123",
=======
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

# Test database URL (SQLite in memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    return TestClient(app)

@pytest.fixture
def test_user_data():
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "role": "buyer"
    }

@pytest.fixture
def test_seller_data():
    return {
        "email": "seller@example.com",
        "password": "sellerpassword123",
>>>>>>> c3ccc0e (refactor: update services, repositories, and API layer structure)
        "role": "seller"
    }

@pytest.fixture
<<<<<<< HEAD
def test_user_buyer(client):
    return {
        "email": "tester2_new@gmail.com",
        "password": "securepassword1234",
        "role": "buyer"
    }
=======
def test_product_data():
    return {
        "name": "Test Product",
        "quantity": 10,
        "price": 29.99
    }
>>>>>>> c3ccc0e (refactor: update services, repositories, and API layer structure)

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_user_data():
    return {
        "email": "buyer@example.com",
        "password": "securepassword123",
        "role": "buyer"
    }


@pytest.fixture
def test_seller_data():
    return {
        "email": "seller@example.com",
        "password": "securepassword123",
        "role": "seller"
    }


@pytest.fixture
def test_product_data():
    return {
        "name": "Test Product",
        "description": "Test description",
        "price": 100,
        "stock": 10,
        "category": "electronics"
    }

# app/tests/conftest.py
import pytest
from app.tests.database import setup_database, db_session, client


@pytest.fixture
def test_user_data():
    return {"email": "buyer@example.com", "password": "securepassword123", "role": "buyer"}


@pytest.fixture
def test_seller_data():
    return {"email": "seller@example.com", "password": "securepassword123", "role": "seller"}


@pytest.fixture
def test_user_seller():
    return {"email": "seller@example.com", "password": "securepassword123", "role": "seller"}


@pytest.fixture
def test_product_data():
    return {"name": "Test Product", "description": "Test description", "price": 100.0, "stock": 10, "category": "electronics"}
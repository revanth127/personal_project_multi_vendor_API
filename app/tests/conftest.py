import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_user_seller():
    return {
        "email": "tester_new@gmail.com",
        "password": "securepassword123",
        "role": "seller"
    }


@pytest.fixture
def test_user_buyer():
    return {
        "email": "tester2_new@gmail.com",
        "password": "securepassword1234",
        "role": "buyer"
    }

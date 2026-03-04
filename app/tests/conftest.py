import pytest

@pytest.fixture
def test_user_seller(client):
    return {
        "email": "tester_new@gmail.com",
        "password": "securepassword123",
        "role": "seller"
    }

@pytest.fixture
def test_user_buyer(client):
    return {
        "email": "tester2_new@gmail.com",
        "password": "securepassword1234",
        "role": "buyer"
    }
import pytest
from fastapi.testclient import TestClient

def test_login_success(client: TestClient, test_user_data):
    # First register a user
    client.post("/api/v1/users/register", json=test_user_data)
    
    # Then login
    login_data = {
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient):
    login_data = {
        "username": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]

def test_register_user(client: TestClient, test_user_data):
    response = client.post("/api/v1/users/register", json=test_user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["role"] == test_user_data["role"]
    assert "id" in data
    assert "password" not in data  # Password should not be in response

def test_register_duplicate_email(client: TestClient, test_user_data):
    # Register user first time
    client.post("/api/v1/users/register", json=test_user_data)
    
    # Try to register same email again
    response = client.post("/api/v1/users/register", json=test_user_data)
    
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

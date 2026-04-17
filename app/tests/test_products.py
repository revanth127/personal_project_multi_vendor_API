import pytest
from fastapi.testclient import TestClient

def get_auth_headers(client: TestClient, user_data: dict):
    """Helper function to get authentication headers"""
    # Register user
    client.post("/api/v1/users/register", json=user_data)
    
    # Login
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}

def test_create_product_success(client: TestClient, test_seller_data, test_product_data):
    headers = get_auth_headers(client, test_seller_data)
    
    response = client.post("/api/v1/products/", json=test_product_data, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == test_product_data["name"]
    assert data["price"] == test_product_data["price"]
    assert data["stock"] == test_product_data["quantity"]

def test_create_product_unauthorized_buyer(client: TestClient, test_user_data, test_product_data):
    headers = get_auth_headers(client, test_user_data)
    
    response = client.post("/api/v1/products/", json=test_product_data, headers=headers)
    
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]

def test_browse_products(client: TestClient, test_seller_data, test_product_data):
    # Create a seller and product
    headers = get_auth_headers(client, test_seller_data)
    client.post("/api/v1/products/", json=test_product_data, headers=headers)
    
    # Browse products (no auth required)
    response = client.get("/api/v1/products/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == test_product_data["name"]

def test_browse_products_with_filters(client: TestClient, test_seller_data, test_product_data):
    # Create a seller and product
    headers = get_auth_headers(client, test_seller_data)
    product_response = client.post("/api/v1/products/", json=test_product_data, headers=headers)
    product_id = product_response.json()["id"]
    
    # Test filtering by seller_id
    response = client.get(f"/api/v1/products/?seller_id={product_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_update_product(client: TestClient, test_seller_data, test_product_data):
    headers = get_auth_headers(client, test_seller_data)
    
    # Create product
    create_response = client.post("/api/v1/products/", json=test_product_data, headers=headers)
    product_id = create_response.json()["id"]
    
    # Update product
    update_data = {"name": "Updated Product", "price": 39.99}
    response = client.put(f"/api/v1/products/{product_id}", json=update_data, headers=headers)
    
    assert response.status_code == 200
    assert "success" in response.json()["status"]

def test_delete_product(client: TestClient, test_seller_data, test_product_data):
    headers = get_auth_headers(client, test_seller_data)
    
    # Create product
    create_response = client.post("/api/v1/products/", json=test_product_data, headers=headers)
    product_id = create_response.json()["id"]
    
    # Delete product
    response = client.delete(f"/api/v1/products/{product_id}", headers=headers)
    
    assert response.status_code == 204

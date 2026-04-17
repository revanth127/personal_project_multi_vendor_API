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

def test_place_order_success(client: TestClient, test_seller_data, test_user_data, test_product_data):
    # Create seller and product
    seller_headers = get_auth_headers(client, test_seller_data)
    product_response = client.post("/api/v1/products/", json=test_product_data, headers=seller_headers)
    product_id = product_response.json()["id"]
    
    # Create buyer and place order
    buyer_headers = get_auth_headers(client, test_user_data)
    response = client.post(f"/api/v1/orders/buy/{product_id}?quantity=2", headers=buyer_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == product_id
    assert data["quantity"] == 2

def test_place_order_unauthorized_seller(client: TestClient, test_seller_data, test_product_data):
    # Create seller and product
    seller_headers = get_auth_headers(client, test_seller_data)
    product_response = client.post("/api/v1/products/", json=test_product_data, headers=seller_headers)
    product_id = product_response.json()["id"]
    
    # Try to buy own product as seller
    response = client.post(f"/api/v1/orders/buy/{product_id}?quantity=1", headers=seller_headers)
    
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]

def test_place_order_insufficient_stock(client: TestClient, test_seller_data, test_user_data, test_product_data):
    # Create seller and product with low stock
    seller_headers = get_auth_headers(client, test_seller_data)
    low_stock_product = {**test_product_data, "quantity": 1}
    product_response = client.post("/api/v1/products/", json=low_stock_product, headers=seller_headers)
    product_id = product_response.json()["id"]
    
    # Try to buy more than available
    buyer_headers = get_auth_headers(client, test_user_data)
    response = client.post(f"/api/v1/orders/buy/{product_id}?quantity=5", headers=buyer_headers)
    
    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]

def test_get_user_orders(client: TestClient, test_seller_data, test_user_data, test_product_data):
    # Create seller and product
    seller_headers = get_auth_headers(client, test_seller_data)
    product_response = client.post("/api/v1/products/", json=test_product_data, headers=seller_headers)
    product_id = product_response.json()["id"]
    
    # Create buyer and place order
    buyer_headers = get_auth_headers(client, test_user_data)
    client.post(f"/api/v1/orders/buy/{product_id}?quantity=1", headers=buyer_headers)
    
    # Get user's orders
    response = client.get("/api/v1/orders/", headers=buyer_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_update_order_status(client: TestClient, test_seller_data, test_user_data, test_product_data):
    # Create seller and product
    seller_headers = get_auth_headers(client, test_seller_data)
    product_response = client.post("/api/v1/products/", json=test_product_data, headers=seller_headers)
    product_id = product_response.json()["id"]
    
    # Create buyer and place order
    buyer_headers = get_auth_headers(client, test_user_data)
    order_response = client.post(f"/api/v1/orders/buy/{product_id}?quantity=1", headers=buyer_headers)
    order_id = order_response.json()["order_id"]
    
    # Seller updates order status
    response = client.put(f"/api/v1/orders/{order_id}/status?new_status=confirmed", headers=seller_headers)
    
    assert response.status_code == 200
    assert "success" in response.json()["status"]

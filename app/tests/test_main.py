from .database import client

def test_create_user(client,test_user_data):
    res=client.post(
        "/api/v1/users/register",json=test_user_data
    ) 
        
    assert res.status_code == 201, f'error{res.text}'

def test_login_user(client, test_user_seller):
    # Register first
    client.post("/api/v1/users/register", json=test_user_seller)
    
    # Then login
    res = client.post(
        '/api/v1/auth/login',
        data={
            "username": test_user_seller["email"],
            "password": test_user_seller["password"]
        }
    )
    assert res.status_code == 200, f'error{res.text}'



from .database import client

def test_create_user(client,test_user_seller):
    res=client.post(
        '/users/register',json=test_user_seller
    ) 
        
    assert res.status_code == 201, f'error{res.text}'

def test_login_user(client,test_user_seller):
    res=client.post(
        '/login',data = {"username":test_user_seller["email"],
                         "password":test_user_seller["password"]} 
    )

    assert res.status_code == 200, f'error{res.text}'
    token_data = res.json()
    assert "access_token" in  token_data
    assert token_data["token_type"] == "bearer"



from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    res = client.post(
        "/api/v1/users/register",
        json={
            "email": "tester2@gmail.com",
            "password": "securepassword123",
            "role": "seller"
        }
    )

    if res.status_code == 422:
        print(res.json())

    assert res.status_code == 201
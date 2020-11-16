from tests import client


def test_get_token_bad_credentials(client):
    login_details = {"email": "123@mail.com", "password": "123123"}
    response = client.post("/api/v1/token", json=login_details)
    assert response.status_code == 401
    assert b"Could not validate credentials" in response.data


def test_get_token(client):
    new_user = {"email": "john@mail.com", "password": "password"}
    user_response = client.post("/api/v1/users", json=new_user)
    assert user_response.status_code == 201
    response = client.post("/api/v1/token", json=new_user)
    assert response.status_code == 200
    assert 'access_token' in response.json and response.json['access_token']

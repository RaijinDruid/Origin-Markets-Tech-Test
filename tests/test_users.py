from tests import client

def test_empty_users(client):
    response = client.get('/api/v1/users')
    assert response.status_code == 200
    assert response.json == []

def test_create_user_bad_password(client):
    user = {"email": "123@mail.com", "password": [123123]}
    response = client.post('/api/v1/users', json=user)
    assert response.status_code == 400
    assert b"str type expected" in response.data and b"password" in response.data

def test_create_user_invalid_email(client):
    user = {"email": "@mail.comSm@mail.com", "password": "pkkpokpok"}
    response = client.post('/api/v1/users', json=user)
    assert response.status_code == 400
    assert b"The email address is not valid" in response.data

def test_create_user(client):
    user = {"email": "john123@mail.com", "password": "mysecretpassword"}
    response = client.post('/api/v1/users', json=user)
    assert response.status_code == 201
    assert response.json['msg'] == "Successfully created new user"
    assert 'access_token' in response.json['data'] and response.json['data']['access_token'] != ""
    assert response.json['data']['user'] == {"email": "john123@mail.com", "id": 1}
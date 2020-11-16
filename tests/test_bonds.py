from tests import client


bond = {
    "isin": "FR0000131104",
    "size": 10021000000,
    "currency": "EUR",
    "maturity": "2025-02-28",
    "lei": "R0MUWSFPU8MPRO8K5P83"
}


def __create_user(client, user={"email": "john@mail.com", "password": "password"}):
    user_response = client.post("/api/v1/users", json=user)
    assert user_response.status_code == 201
    return user_response.json['data']


def test_create_bond_no_auth_token(client):
    response = client.post("/api/v1/bonds", json=bond)
    assert response.status_code == 401
    assert b"Not authorized, please send a valid auth token" in response.data


def test_create_bond_invalid_auth_token(client):
    response = client.post("/api/v1/bonds", json=bond, headers={"Authorization": "WrongAuthToken"})
    assert response.status_code == 401
    assert b"Could not validate credentials" in response.data


def test_create_bad_bond(client):
    invalid_bond = bond.copy()
    token = __create_user(client)['access_token']
    # set size to be a str, schema defines size -> int
    invalid_bond['size'] = "WRONGFORMAT"
    bond_response = client.post("/api/v1/bonds", json=invalid_bond, headers={'Authorization': token})
    assert bond_response.status_code == 400
    assert b"validation_error" in bond_response.data
    assert b"value is not a valid integer" in bond_response.data and b"size" in bond_response.data


def test_create_bond(client):
    token = __create_user(client)['access_token']
    bond_response = client.post("/api/v1/bonds", json=bond, headers={'Authorization': token})
    assert bond_response.status_code == 200
    assert bond_response.json == {
        "id": 1,
        "isin": "FR0000131104",
        "size": 10021000000,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "R0MUWSFPU8MPRO8K5P83",
        "user_id": 1,
        "legal_name": "BNP PARIBAS"
    }


def test_get_bonds_bad_creds(client):
    response = client.get("/api/v1/bonds")
    assert response.status_code == 401
    assert b"Not authorized, please send a valid auth token" in response.data
    token = __create_user(client)['access_token']
    response = client.get("/api/v1/bonds", json=bond, headers={"Authorization": "WrongAuthToken"})
    assert response.status_code == 401
    assert b"Could not validate credentials" in response.data


def test_get_bonds(client):
    user = __create_user(client)
    token = user['access_token']
    bond_2 = bond.copy()
    bond_2['currency'] = "GBP"

    create_bond_1_resp = client.post("/api/v1/bonds", json=bond, headers={'Authorization': token})
    assert create_bond_1_resp.status_code == 201
    create_bond_2_resp = client.post("/api/v1/bonds", json=bond_2, headers={'Authorization': token})
    assert create_bond_2_resp.status_code == 201
    get_bond_response = client.get("/api/v1/bonds", headers={"Authorization": token})
    assert get_bond_response.status_code == 200
    assert get_bond_response.json == [
        {
            "id": 1,
            "isin": "FR0000131104",
            "size": 10021000000,
            "currency": "EUR",
            "maturity": "2025-02-28",
            "lei": "R0MUWSFPU8MPRO8K5P83",
            "legal_name": "BNP PARIBAS",
            "user_id": 1
        }, {
            "id": 2,
            "isin": "FR0000131104",
            "size": 10021000000,
            "currency": "GBP",
            "maturity": "2025-02-28",
            "lei": "R0MUWSFPU8MPRO8K5P83",
            "legal_name": "BNP PARIBAS",
            "user_id": 1
        }
    ]

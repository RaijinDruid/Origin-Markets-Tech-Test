# Origin Markets Technical Test

Python technical test for origin markets.
I have completed the task using: flask, SQLALCHEMY, Pydantic, Pytest

### Spec:

We would like you to implement an api to: ingest some data representing bonds, query an external api for some additional data, store the result, and make the resulting data queryable via api.

Fork this hello world repo leveraging Django & Django Rest Framework. (If you wish to use something else like flask that's fine too.)
Please pick and use a form of authentication, so that each user will only see their own data. (DRF Auth Options)
We are missing some data! Each bond will have a lei field (Legal Entity Identifier). Please use the GLEIF API to find the corresponding Legal Name of the entity which issued the bond.
If you are using a database, SQLite is sufficient.
Please test any additional logic you add.

## How to run

`pip install -r requirements.txt` to install packages\
`python3 main.py` to run server.\
`pytest -s` to run tests.

## API

The following outlines the API:

### USERS

Send a request to

```python
POST /api/v1/users
```

to create a new user that will be needed in order to create/retrieve bonds, with data that looks like:

```json
{
  "email": "john@mail.com",
  "password": "password"
}
```

The response data for successfully creating a new user will contain:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyX2lkOjEiLCJleHAiOjE2MDU1MjkzOTR9.tCiXmsFd4eGH2bfCog5O9CbKstxlmo452s4aPYRnP98",
  "user": {
    "email": "john@mail.com",
    "id": 1
  }
}
```

This access_token you will need as an 'Authorization' header when sending requests:

```python
POST /api/v1/bonds
GET /api/v1/bonds
```

### TOKENS

You can send a request to

```python
POST /api/v1/token
```

with the email and password of your user account to get a new access_token.

### BONDS

You can send a request to:

```python
POST /api/v1/bonds
```

to create a "bond" with data that looks like:

```json
{
  "isin": "FR0000131104",
  "size": 100000000,
  "currency": "EUR",
  "maturity": "2025-02-28",
  "lei": "R0MUWSFPU8MPRO8K5P83"
}
```

You can send a request to:

```python
GET /api/v1/bonds
```

to see some data like this:

```json
{
  "currency": "EUR",
  "id": 1,
  "isin": "FR0000131104",
  "legal_name": "BNP PARIBAS",
  "lei": "R0MUWSFPU8MPRO8K5P83",
  "maturity": "2025-02-28",
  "size": 10021000000,
  "user_id": 1
}
```

Sending a request to with the query parameter "legal_name"

```python
GET /api/v1/bonds?legal_name=BNPPARIBAS
```

will filter down results with a legal_name = to parameter value

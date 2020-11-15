
from project.app import create_app
import os
import pytest


@pytest.fixture
def client():
    app = create_app(config_mode="Test")
    with app.test_client() as client:
        yield client

    # remove data in test database
    from project.database import clear_db
    clear_db()

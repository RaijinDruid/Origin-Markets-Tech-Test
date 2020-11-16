
from project.app import create_app
import os
import pytest


@pytest.fixture
def client():
    test_config = {
        "SQLALCHEMY_DATABASE_URL": "sqlite:///./test-sqlite.db",
        "ENV": "development",
        "DEBUG": True,
        "SECRET_KEY": "would-get-from-env-file"
    }
    app = create_app(test_config)
    with app.test_client() as client:
        yield client

    # remove data in test database
    from project.database import clear_db
    clear_db()

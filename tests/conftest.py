import os
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("LOCAL_BEARER_TOKEN", "secret_token")

from app.main import app

@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture()
def auth_headers():
    return {"Authorization": "Bearer secret_token"}
from fastapi.testclient import TestClient

from src.main import app


def test_client() -> TestClient:
    return TestClient(app)


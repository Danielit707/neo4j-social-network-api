from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to the Social Network API!"


def test_expected_routes_are_registered():
    paths = {route.path for route in app.routes}
    assert "/health" in paths
    assert "/analytics/summary" in paths
    assert "/analytics/me" in paths

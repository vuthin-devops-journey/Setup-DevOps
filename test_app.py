import pytest
from app import app


@pytest.fixture
def client():
    """Create test client to call API without running real server"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_status_code(client):
    """GET / should return 200"""
    response = client.get("/")
    assert response.status_code == 200


def test_home_message(client):
    """GET / should have running status"""
    data = client.get("/").get_json()
    assert data["status"] == "running"
    assert "message" in data


def test_health_status_code(client):
    """GET /health should return 200"""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response(client):
    """GET /health should return healthy + timestamp"""
    data = client.get("/health").get_json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_version_response(client):
    """GET /version should return correct version"""
    data = client.get("/version").get_json()
    assert data["version"] == "2.0.0"
    assert data["app"] == "devops-journey"


def test_not_found(client):
    """Unknown route should return 404"""
    response = client.get("/does-not-exist")
    assert response.status_code == 404


def test_visits_increments(client):
    """GET /visits should return incrementing count"""
    first = client.get("/visits").get_json()["total_visits"]
    second = client.get("/visits").get_json()["total_visits"]
    assert second == first + 1


def test_visits_status_code(client):
    """GET /visits should return 200"""
    response = client.get("/visits")
    assert response.status_code == 200


def test_metrics_status_code(client):
    """GET /metrics should return 200"""
    response = client.get("/metrics")
    assert response.status_code == 200


def test_metrics_contains_request_counter(client):
    """Metrics should expose flask_http_request_total counter"""
    response = client.get("/metrics")
    assert b"flask_http_request_total" in response.data


def test_metrics_contains_app_info(client):
    """Metrics should expose custom app_info with version"""
    response = client.get("/metrics")
    assert b"app_info" in response.data
    assert b'version="2.0.0"' in response.data

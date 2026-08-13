import pytest
from app import app


@pytest.fixture
def client():
    """បង្កើត test client សម្រាប់ call API ដោយមិនចាំបាច់ run server ពិត"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_status_code(client):
    """Test: GET / ត្រូវ return 200"""
    response = client.get("/")
    assert response.status_code == 200


def test_home_message(client):
    """Test: GET / ត្រូវមាន status running"""
    data = client.get("/").get_json()
    assert data["status"] == "running"
    assert "message" in data


def test_health_status_code(client):
    """Test: GET /health ត្រូវ return 200"""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response(client):
    """Test: GET /health ត្រូវ return healthy + timestamp"""
    data = client.get("/health").get_json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_version_response(client):
    """Test: GET /version ត្រូវ return version ត្រឹមត្រូវ"""
    data = client.get("/version").get_json()
    assert data["version"] == "1.0.0"
    assert data["app"] == "devops-journey"


def test_not_found(client):
    """Test: route មិនមាន ត្រូវ return 404"""
    response = client.get("/does-not-exist")
    assert response.status_code == 404

def test_visits_increments(client):
    """Test: /visits ត្រូវ return count ដែលកើនឡើង"""
    first = client.get("/visits").get_json()["total_visits"]
    second = client.get("/visits").get_json()["total_visits"]
    assert second == first + 1


def test_visits_status_code(client):
    """Test: GET /visits ត្រូវ return 200"""
    response = client.get("/visits")
    assert response.status_code == 200

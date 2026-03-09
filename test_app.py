import pytest
from app import app, init_db

@pytest.fixture
def client():
    init_db()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Benchmark: Validates internal logic before build stage."""
    res = client.get('/health')
    assert res.status_code == 200
    assert b"Online" in res.data

def test_db_retrieval(client):
    """Benchmark: Ensures database integrity within the container."""
    res = client.get('/clients')
    assert res.status_code == 200
    assert len(res.json) >= 1

def test_add_client_logic(client):
    """Benchmark: Validates POST method functionality."""
    payload = {"name": "DevOps_User", "program": "Elite"}
    res = client.post('/add_client', json=payload)
    assert res.status_code == 201
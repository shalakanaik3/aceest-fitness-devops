import pytest
from app import app, init_db

@pytest.fixture
def client():
    init_db()
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    res = client.get('/health')
    assert res.status_code == 200
    assert res.json['status'] == 'healthy'

def test_get_clients(client):
    res = client.get('/clients')
    assert res.status_code == 200
    assert len(res.json) > 0
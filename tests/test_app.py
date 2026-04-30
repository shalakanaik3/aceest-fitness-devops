import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the base route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"ACEest Fitness" in response.data

def test_get_members(client):
    """Test member retrieval."""
    response = client.get('/members')
    assert response.status_code == 200
    assert len(response.json) >= 2
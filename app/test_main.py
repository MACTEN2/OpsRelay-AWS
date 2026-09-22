from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.0.0"}

def test_chaos_trigger():
    # Trigger chaos
    response = client.post("/chaos")
    assert response.status_code == 200
    
    # Check that /health now fails
    health_response = client.get("/health")
    assert health_response.status_code == 500

    # Recover app for other tests
    recover_response = client.post("/recover")
    assert recover_response.status_code == 200
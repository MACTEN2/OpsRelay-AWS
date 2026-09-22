from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.1.0"}

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_requests" in data
    assert "error_rate_pct" in data

def test_log_level_change():
    response = client.post("/log-level", json={"level": "DEBUG"})
    assert response.status_code == 200
    assert response.json()["message"] == "Log level updated to DEBUG"

def test_chaos_and_recovery():
    # Trigger chaos
    client.post("/chaos")
    assert client.get("/health").status_code == 500

    # Recover app
    client.post("/recover")
    assert client.get("/health").status_code == 200
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def sample_leads():
    return [
        {"name": "Acme Corp", "engagement": 80, "activity": 90},
        {"name": "Beta Inc", "engagement": 70, "activity": 85},
    ]

def test_score_leads_valid_input(sample_leads):
    response = client.post("/api/score_leads", json=sample_leads)
    assert response.status_code == 200
    data = response.json()
    assert "scores" in data
    assert len(data["scores"]) == len(sample_leads)

def test_score_leads_empty_input():
    response = client.post("/api/score_leads", json=[])
    assert response.status_code == 400
    assert response.json()["detail"] == "No leads provided."

def test_score_leads_invalid_input():
    response = client.post("/api/score_leads", json={"invalid": "data"})
    assert response.status_code == 422
    assert "detail" in response.json()
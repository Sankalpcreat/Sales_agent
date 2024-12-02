import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_lead_suggestions_valid_input():
    payload = {
        "query_vector": [0.1, 0.2, 0.3, 0.4],
        "top_k": 5
    }
    response = client.post("/api/lead_suggestions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) <= 5

def test_lead_suggestions_missing_vector():
    payload = {"top_k": 5}
    response = client.post("/api/lead_suggestions", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid query vector provided."

def test_lead_suggestions_empty_vector():
    payload = {
        "query_vector": [],
        "top_k": 5
    }
    response = client.post("/api/lead_suggestions", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid query vector provided."
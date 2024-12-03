import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_follow_up_valid_input():
    payload = {
        "lead_id": 1,
        "follow_up_time": "2024-12-05T10:00:00",
        "message": "Follow-up with Acme Corp",
    }
    response = client.post("/api/follow_up", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Follow-up scheduled successfully."

def test_follow_up_missing_fields():
    payload = {"lead_id": 1, "follow_up_time": "2024-12-05T10:00:00"}
    response = client.post("/api/follow_up", json=payload)
    assert response.status_code == 422  
    assert "field required" in response.json()["detail"][0]["msg"].lower()

def test_follow_up_invalid_date():
    payload = {
        "lead_id": 1,
        "follow_up_time": "invalid-date",
        "message": "Follow-up with Acme Corp",
    }
    response = client.post("/api/follow_up", json=payload)
    assert response.status_code == 422
    assert "Invalid date format" in response.json()["detail"]
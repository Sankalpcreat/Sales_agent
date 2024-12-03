import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def sample_leads_payload():
    return {
        "leads": [
            {"name": "Acme Corp", "engagement": 80, "activity": 90},
            {"name": "Beta Inc", "engagement": 70, "activity": 85},
        ]
    }

def test_score_leads_valid_input(sample_leads_payload):
    print("\n=== Testing Score Leads Valid Input ===")
    print(f"Request Payload: {sample_leads_payload}")
    response = client.post("/api/score_leads", json=sample_leads_payload)
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert "scores" in data
    assert len(data["scores"]) == len(sample_leads_payload["leads"])

def test_score_leads_empty_input():
    print("\n=== Testing Score Leads Empty Input ===")
    print("Request Payload: Empty leads list")
    response = client.post("/api/score_leads", json={"leads": []})
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {response.json()}")
    assert response.status_code == 400
    assert response.json()["detail"] == "No leads provided."

def test_score_leads_invalid_input():
    invalid_payload = {"invalid": "data"}
    print("\n=== Testing Score Leads Invalid Input ===")
    print(f"Request Payload: {invalid_payload}")
    response = client.post("/api/score_leads", json=invalid_payload)
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {response.json()}")
    assert response.status_code == 422
    assert "detail" in response.json()
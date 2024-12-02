import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate_proposal_valid_input():
    payload = {
        "client_name": "Acme Corp",
        "requirements": "Cloud collaboration tools for remote teams",
    }
    response = client.post("/api/proposal", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "proposal" in data
    assert len(data["proposal"]) > 0

def test_generate_proposal_missing_fields():
    payload = {"client_name": "Acme Corp"}
    response = client.post("/api/proposal", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Client name and requirements are required."

def test_generate_proposal_empty_input():
    response = client.post("/api/proposal", json={})
    assert response.status_code == 400
    assert response.json()["detail"] == "Client name and requirements are required."

def test_generate_proposal_invalid_input():
    payload = {"client_name": 123, "requirements": []}
    response = client.post("/api/proposal", json=payload)
    assert response.status_code == 422
    assert "detail" in response.json()
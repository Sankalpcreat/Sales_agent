import pytest
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_generate_proposal_valid_input():
    payload = {
        "client_name": "Acme Corp",
        "requirements": "Cloud collaboration tools for remote teams",
    }
    print("\n=== Testing Generate Proposal Valid Input ===")
    print("Request Payload:")
    print(json.dumps(payload, indent=2))
    
    response = client.post("/api/proposal", json=payload)
    
    print(f"Response Status: {response.status_code}")
    try:
        response_json = response.json()
        print("Response Body:")
        print(json.dumps(response_json, indent=2))
    except Exception as e:
        print(f"Error parsing response: {e}")
        print("Response Text:", response.text)
    
    assert response.status_code == 200
    data = response.json()
    assert "proposal" in data
    assert len(data["proposal"]) > 0

def test_generate_proposal_missing_fields():
    payload = {"client_name": "Acme Corp"}
    print("\n=== Testing Generate Proposal Missing Fields ===")
    print("Request Payload:")
    print(json.dumps(payload, indent=2))
    
    response = client.post("/api/proposal", json=payload)
    
    print(f"Response Status: {response.status_code}")
    try:
        response_json = response.json()
        print("Response Body:")
        print(json.dumps(response_json, indent=2))
    except Exception as e:
        print(f"Error parsing response: {e}")
        print("Response Text:", response.text)
    
    assert response.status_code == 422
    assert "field required" in response.json()["detail"][0]["msg"].lower()

def test_generate_proposal_empty_input():
    print("\n=== Testing Generate Proposal Empty Input ===")
    print("Request Payload: {}")
    
    response = client.post("/api/proposal", json={})
    
    print(f"Response Status: {response.status_code}")
    try:
        response_json = response.json()
        print("Response Body:")
        print(json.dumps(response_json, indent=2))
    except Exception as e:
        print(f"Error parsing response: {e}")
        print("Response Text:", response.text)
    
    assert response.status_code == 422
    assert "field required" in response.json()["detail"][0]["msg"].lower()

def test_generate_proposal_invalid_input():
    payload = {"client_name": 123, "requirements": []}
    print("\n=== Testing Generate Proposal Invalid Input ===")
    print("Request Payload:")
    print(json.dumps(payload, indent=2))
    
    response = client.post("/api/proposal", json=payload)
    
    print(f"Response Status: {response.status_code}")
    try:
        response_json = response.json()
        print("Response Body:")
        print(json.dumps(response_json, indent=2))
    except Exception as e:
        print(f"Error parsing response: {e}")
        print("Response Text:", response.text)
    
    assert response.status_code == 422
    assert "detail" in response.json()
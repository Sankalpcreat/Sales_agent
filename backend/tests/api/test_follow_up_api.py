import pytest
from fastapi.testclient import TestClient
from main import app
import json
from datetime import datetime, timedelta

client = TestClient(app)

def get_future_datetime(hours=1):
    """Generate a future datetime string."""
    future_time = datetime.now() + timedelta(hours=hours)
    return future_time.strftime("%Y-%m-%dT%H:%M:%S")

def test_follow_up_valid_input():
    payload = {
        "lead_id": 1,
        "follow_up_time": get_future_datetime(),
        "message": "Follow-up with Acme Corp",
    }
    print("\n=== Testing Follow Up Valid Input ===")
    print("Request Payload:")
    print(json.dumps(payload, indent=2))
    
    response = client.post("/api/follow_up", json=payload)
    
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
    assert data["message"] == "Follow-up scheduled successfully."

def test_follow_up_missing_fields():
    payload = {"lead_id": 1, "follow_up_time": get_future_datetime()}
    print("\n=== Testing Follow Up Missing Fields ===")
    print("Request Payload:")
    print(json.dumps(payload, indent=2))
    
    response = client.post("/api/follow_up", json=payload)
    
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

def test_follow_up_invalid_date():
    payload = {
        "lead_id": 1,
        "follow_up_time": "invalid-date",
        "message": "Follow-up with Acme Corp",
    }
    print("\n=== Testing Follow Up Invalid Date ===")
    print("Request Payload:")
    print(json.dumps(payload, indent=2))
    
    response = client.post("/api/follow_up", json=payload)
    
    print(f"Response Status: {response.status_code}")
    try:
        response_json = response.json()
        print("Response Body:")
        print(json.dumps(response_json, indent=2))
    except Exception as e:
        print(f"Error parsing response: {e}")
        print("Response Text:", response.text)
    
    assert response.status_code == 422
    assert "Invalid date format" in response.json()["detail"]
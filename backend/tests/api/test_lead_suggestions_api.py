import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
import json

client = TestClient(app)

@pytest.fixture
def sample_query_vector():
    # Create a vector of the expected dimension (128)
    return [0.1] * 128

@pytest.fixture
def sample_recommendations():
    return [
        {"id": 1, "name": "Lead 1", "score": 0.95},
        {"id": 2, "name": "Lead 2", "score": 0.85}
    ]

@patch('agents.lead_suggestions.LeadSuggestionsAgent.recommend_similar_leads')
def test_lead_suggestions_valid_input(mock_recommend, sample_query_vector, sample_recommendations):
    # Mock the recommendation method to return predefined recommendations
    mock_recommend.return_value = sample_recommendations

    payload = {
        "query_vector": sample_query_vector,
        "top_k": 5
    }
    print("\n=== Testing Lead Suggestions Valid Input ===")
    print(f"Request Payload: {json.dumps(payload, indent=2)}")
    response = client.post("/api/lead_suggestions", json=payload)
    print(f"Response Status: {response.status_code}")
    
    # Print full response details
    try:
        response_json = response.json()
        print("Response Body (Formatted):")
        print(json.dumps(response_json, indent=2))
    except Exception as e:
        print(f"Error parsing response: {e}")
        print("Response Text:", response.text)
    
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert data["recommendations"] == sample_recommendations

def test_lead_suggestions_missing_vector():
    payload = {"top_k": 5}
    print("\n=== Testing Lead Suggestions Missing Vector ===")
    print(f"Request Payload: {json.dumps(payload, indent=2)}")
    response = client.post("/api/lead_suggestions", json=payload)
    print(f"Response Status: {response.status_code}")
    
    # Print full response details
    try:
        response_json = response.json()
        print("Response Body (Formatted):")
        print(json.dumps(response_json, indent=2))
    except Exception as e:
        print(f"Error parsing response: {e}")
        print("Response Text:", response.text)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid query vector provided."

def test_lead_suggestions_empty_vector():
    payload = {
        "query_vector": [],
        "top_k": 5
    }
    print("\n=== Testing Lead Suggestions Empty Vector ===")
    print(f"Request Payload: {json.dumps(payload, indent=2)}")
    response = client.post("/api/lead_suggestions", json=payload)
    print(f"Response Status: {response.status_code}")
    
    # Print full response details
    try:
        response_json = response.json()
        print("Response Body (Formatted):")
        print(json.dumps(response_json, indent=2))
    except Exception as e:
        print(f"Error parsing response: {e}")
        print("Response Text:", response.text)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid query vector provided."
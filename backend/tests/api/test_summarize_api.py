import pytest
import json
import os
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Voice file path
TEST_AUDIO_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_audio_mono.wav")

def test_summarize_valid_audio_file():
    print("\n=== Testing Summarize Valid Audio File ===")
    print(f"Using audio file at: {TEST_AUDIO_PATH}")
    
    if not os.path.exists(TEST_AUDIO_PATH):
        pytest.skip(f"Test audio file not found at {TEST_AUDIO_PATH}")
    
    with open(TEST_AUDIO_PATH, "rb") as audio_file:
        print("Uploading test audio file...")
        files = {"file": ("test_audio_mono.wav", audio_file, "audio/wav")}
        response = client.post("/api/summarize", files=files)
        
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
        assert "summary" in data
        assert len(data["summary"]) > 0
        assert not data["summary"].startswith("Error")

def test_summarize_missing_file():
    print("\n=== Testing Summarize Missing File ===")
    print("Sending request without file...")
    
    response = client.post("/api/summarize")
    
    print(f"Response Status: {response.status_code}")
    try:
        response_json = response.json()
        print("Response Body:")
        print(json.dumps(response_json, indent=2))
    except Exception as e:
        print(f"Error parsing response: {e}")
        print("Response Text:", response.text)
    
    assert response.status_code == 422  # FastAPI's default validation error code
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "missing"
    assert "file" in error_detail["loc"]

def test_summarize_invalid_file_type():
    test_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_invalid.txt")
    print("\n=== Testing Summarize Invalid File Type ===")
    
    # Create a temporary test file if it doesn't exist
    if not os.path.exists(test_file_path):
        with open(test_file_path, "w") as f:
            f.write("This is not an audio file")
    
    with open(test_file_path, "rb") as invalid_file:
        print("Uploading invalid file type...")
        files = {"file": ("test_invalid.txt", invalid_file, "text/plain")}
        response = client.post("/api/summarize", files=files)
        
        print(f"Response Status: {response.status_code}")
        try:
            response_json = response.json()
            print("Response Body:")
            print(json.dumps(response_json, indent=2))
        except Exception as e:
            print(f"Error parsing response: {e}")
            print("Response Text:", response.text)
        
        assert response.status_code == 400
        assert "Invalid file type" in response.json()["detail"]
    
    # Clean up the temporary file
    if os.path.exists(test_file_path):
        os.remove(test_file_path)

def test_summarize_empty_file():
    print("\n=== Testing Summarize Empty File ===")
    
    # Create an empty file
    files = {"file": ("empty.wav", b"", "audio/wav")}
    print("Uploading empty file...")
    
    response = client.post("/api/summarize", files=files)
    
    print(f"Response Status: {response.status_code}")
    try:
        response_json = response.json()
        print("Response Body:")
        print(json.dumps(response_json, indent=2))
    except Exception as e:
        print(f"Error parsing response: {e}")
        print("Response Text:", response.text)
    
    assert response.status_code == 400
    assert "Empty file" in response.json()["detail"]
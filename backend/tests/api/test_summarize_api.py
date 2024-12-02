import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_summarize_valid_audio_file():
    with open("test/test_audio.wav", "rb") as audio_file:
        response = client.post("/api/summarize", files={"file": audio_file})
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert len(data["summary"]) > 0

def test_summarize_missing_file():
    response = client.post("/api/summarize")
    assert response.status_code == 400
    assert response.json()["detail"] == "No file uploaded."

def test_summarize_invalid_audio_file():
    with open("test/invalid.txt", "rb") as invalid_file:
        response = client.post("/api/summarize", files={"file": invalid_file})
        assert response.status_code == 500
        assert "Error summarizing meeting" in response.json()["detail"]
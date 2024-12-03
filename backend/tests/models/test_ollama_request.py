import pytest
import requests
from models.ollama_request import OllamaApiClient


@pytest.fixture
def ollama_api_client():
    return OllamaApiClient(api_url="http://localhost:11434/api/generate")


def test_query_model_success(mocker, ollama_api_client):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"response": "Mocked model response"}
    mock_response.status_code = 200
    mocker.patch("requests.post", return_value=mock_response)

    prompt = "Generate a summary for the given content."
    model = "llama3.2:latest"

    result = ollama_api_client.query_model(prompt, model)
    assert result == "Mocked model response"
    requests.post.assert_called_once_with(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt},
        timeout=10,
    )


def test_query_model_no_response_key(mocker, ollama_api_client):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {}
    mock_response.status_code = 200
    mocker.patch("requests.post", return_value=mock_response)

    prompt = "Generate a summary for the given content."
    result = ollama_api_client.query_model(prompt)
    assert result == "No response from model."


def test_query_model_request_exception(mocker, ollama_api_client):
    mocker.patch("requests.post", side_effect=requests.exceptions.RequestException("Connection error"))

    prompt = "Generate a summary for the given content."
    result = ollama_api_client.query_model(prompt)
    assert result == "Error querying model: Connection error"


def test_query_model_invalid_status_code(mocker, ollama_api_client):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("HTTP error")
    mocker.patch("requests.post", return_value=mock_response)

    prompt = "Generate a summary for the given content."
    result = ollama_api_client.query_model(prompt)
    assert result == "Error querying model: HTTP error"
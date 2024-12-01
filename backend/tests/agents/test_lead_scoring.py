import pytest
from agents.lead_scoring import LeadScoringAgent
from models.ollama_request import OllamaApiClient

@pytest.fixture
def mock_ollama_api_client(mocker):
    """Mock the OllamaApiClient."""
    mock_service = mocker.Mock(spec=OllamaApiClient)
    mock_service.query_model.return_value = "85"  
    return mock_service

@pytest.fixture
def lead_scoring_agent(mock_ollama_api_client):
    return LeadScoringAgent(mock_ollama_api_client)

def test_score_leads(lead_scoring_agent):
    leads = [
        {"name": "Acme Corp", "engagement": 80, "activity": 90},
        {"name": "Beta Inc", "engagement": 70, "activity": 85},
    ]
    results = lead_scoring_agent.score_leads(leads)

    assert len(results) == 2
    assert results[0]["name"] == "Acme Corp"
    assert results[0]["score"] == "85" 
    assert results[1]["name"] == "Beta Inc"
    assert results[1]["score"] == "85"

def test_empty_leads(lead_scoring_agent):
    leads = []
    results = lead_scoring_agent.score_leads(leads)
    assert results == []

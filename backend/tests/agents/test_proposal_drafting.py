import pytest
from agents.proposal_drafting import ProposalDraftingAgent
from models.ollama_request import OllamaApiClient

@pytest.fixture
def mock_ollama_api_client(mocker):

    mock_client=mocker.Mock(spec=OllamaApiClient)
    mock_client.query_model.return_value="Mock proposal for Acme Corp."
    return mock_client

@pytest.fixture
def proposal_agent(mock_ollama_api_client):

    return ProposalDraftingAgent(mock_ollama_api_client)

def test_generate_proposal(proposal_agent,mock_ollama_api_client):
    client_name="Acme Corp."
    requirements="Cloud collaboration tools for remote teams"

    result=proposal_agent.generate_proposal(client_name,requirements)

    assert result == "Mock proposal for Acme Corp."

    expected_prompt = (
        f"Draft a proposal for the following client:\n"
        f"Client Name:{client_name}\n"
        f"Requirements:{requirements}\n"
        f"Please provide a professional and detailed proposal."
    )
    mock_ollama_api_client.query_model.assert_called_once_with(expected_prompt)

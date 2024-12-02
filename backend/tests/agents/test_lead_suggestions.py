import pytest
import numpy as np
from agents.lead_suggestions import LeadSuggestionsAgent
from core.vector_search import VectorSearchService

@pytest.fixture
def mock_vector_search_service(mocker):
    mock_service = mocker.Mock(spec=VectorSearchService)
    mock_service.search.return_value = (np.array([[1, 2]]), np.array([[0.9, 0.8]]))
    return mock_service

@pytest.fixture
def lead_suggestions_agent(mock_vector_search_service):
    return LeadSuggestionsAgent(mock_vector_search_service)

def test_recommend_similar_leads(lead_suggestions_agent):
    query_vector = np.array([[0.1, 0.2, 0.3, 0.4]])
    top_k = 2

    recommendations = lead_suggestions_agent.recommend_similar_leads(query_vector, top_k)

    assert len(recommendations) == 2
    assert recommendations[0]["lead_id"] == 1
    assert recommendations[0]["similarity"] == 0.9
    assert recommendations[1]["lead_id"] == 2
    assert recommendations[1]["similarity"] == 0.8

def test_invalid_query_vector(lead_suggestions_agent):
    query_vector = "invalid_vector"

    with pytest.raises(TypeError):
        lead_suggestions_agent.recommend_similar_leads(query_vector, top_k=2)

def test_empty_query_vector(lead_suggestions_agent):
    query_vector = np.array([])

    recommendations = lead_suggestions_agent.recommend_similar_leads(query_vector, top_k=2)

    assert recommendations == []

import pytest
import numpy as np
from core.vector_search import VectorSearchService


@pytest.fixture
def vector_search_service():
    return VectorSearchService(vector_size=4)


def test_add_vector(vector_search_service):
    vectors = np.array([[0.1, 0.2, 0.3, 0.4], [0.5, 0.6, 0.7, 0.8]], dtype="float32")
    vector_search_service.add_vector(vectors)
    assert vector_search_service.index.ntotal == 2


def test_search_valid_query(vector_search_service):
    vectors = np.array([[0.1, 0.2, 0.3, 0.4], [0.5, 0.6, 0.7, 0.8]], dtype="float32")
    vector_search_service.add_vector(vectors)

    query_vector = np.array([[0.1, 0.2, 0.3, 0.4]], dtype="float32")
    indices, distances = vector_search_service.search(query_vector, top_k=2)

    assert len(indices[0]) == 2
    assert len(distances[0]) == 2
    assert indices[0][0] == 0  # Most similar vector should be itself


def test_search_empty_index(vector_search_service):
    query_vector = np.array([[0.1, 0.2, 0.3, 0.4]], dtype="float32")
    indices, distances = vector_search_service.search(query_vector, top_k=2)

    assert indices.size == 0
    assert distances.size == 0


def test_add_vector_dimension_mismatch(vector_search_service):
    vectors = np.array([[0.1, 0.2, 0.3]], dtype="float32")  # Only 3 dimensions instead of 4
    
    with pytest.raises(ValueError, match="Input vectors must have dimension"):
        vector_search_service.add_vector(vectors)


def test_search_dimension_mismatch(vector_search_service):
    query_vector = np.array([[0.1, 0.2, 0.3]], dtype="float32")  # Only 3 dimensions instead of 4
    
    with pytest.raises(ValueError, match="Query vector must have dimension"):
        vector_search_service.search(query_vector, top_k=2)
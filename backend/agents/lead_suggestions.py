from core.vector_search import VectorSearchService
import numpy as np

class LeadSuggestionsAgent:
    def __init__(self, vector_search_service: VectorSearchService):
        
        self.vector_search_service = vector_search_service

    def recommend_similar_leads(self, query_vector: np.ndarray, top_k: int = 5) -> list:
        
        if not isinstance(query_vector, np.ndarray):
            raise TypeError("Query vector must be a numpy array")
            
      
        if query_vector.size == 0:
            return []
            
        indices, distances = self.vector_search_service.search(query_vector, top_k)
        return [{"lead_id": int(idx), "similarity": float(dist)} for idx, dist in zip(indices[0], distances[0])]
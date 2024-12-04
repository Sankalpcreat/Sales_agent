from typing import List, Dict, Any
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class VectorSearchService:
    def __init__(self, vector_size: int = 768):
        self._vectors: List[Dict[str, Any]] = []
        self._vector_size = vector_size

    def add_vector(self, vector: List[float], metadata: Dict[str, Any]) -> None:
        self._vectors.append({
            'vector': np.array(vector),
            'metadata': metadata
        })

    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        if not self._vectors:
            return []

        store_vectors = [item['vector'] for item in self._vectors]
        similarities = cosine_similarity(query_vector, store_vectors)[0]
        
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        return [
            {**self._vectors[idx], 'similarity': similarities[idx]} 
            for idx in top_k_indices
        ]
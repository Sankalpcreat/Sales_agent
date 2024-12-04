from typing import Dict, Any, List, Optional
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SharedMemoryService:
    def __init__(self, vector_size: int = 768):
        self._context_store: Dict[str, Any] = {}
        self._vector_store: List[Dict[str, Any]] = []
        self._vector_size = vector_size

    def store_context(self, key: str, context: Dict[str, Any]) -> None:
        self._context_store[key] = context

    def get_context(self, key: str) -> Optional[Dict[str, Any]]:
        return self._context_store.get(key)

    def add_vectors(self, vectors: List[List[float]], metadata: List[Dict[str, Any]]) -> None:
        for vec, meta in zip(vectors, metadata):
            self._vector_store.append({
                'vector': vec,
                'metadata': meta
            })

    def search_vectors(self, query_vector: List[float], k: int = 5) -> List[Dict[str, Any]]:
        if not self._vector_store:
            return []

        store_vectors = [item['vector'] for item in self._vector_store]
        similarities = cosine_similarity(query_vector, store_vectors)[0]
        
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        return [
            {**self._vector_store[idx], 'similarity': similarities[idx]} 
            for idx in top_k_indices
        ]
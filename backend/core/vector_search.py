import faiss
import numpy as np

class VectorSearchService:
    def __init__(self, vector_size: int):
        self.vector_size = vector_size
        self.index = faiss.IndexFlatL2(vector_size)

    def add_vector(self, vectors: np.ndarray):
        if vectors.shape[1] != self.vector_size:
            raise ValueError(f"Input vectors must have dimension {self.vector_size}")
        self.index.add(vectors)

    def search(self, query_vector: np.ndarray, top_k=5):
        if query_vector.shape[1] != self.vector_size:
            raise ValueError(f"Query vector must have dimension {self.vector_size}")
        
        if self.index.ntotal == 0:
            return np.array([]), np.array([])
            
        distances, indices = self.index.search(query_vector, top_k)
        return indices, distances

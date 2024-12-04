from typing import Dict, Any, List
import faiss
import numpy as np
import json
from datetime import datetime

class SharedMemoryService:
    def __init__(self, vector_size: int = 768):
        self.vector_size = vector_size
        self.vector_index = faiss.IndexFlatL2(vector_size)
        self.context_store = {}  # In-memory store for context
        self.vector_metadata = []  # Store metadata for vectors
        
    def store_context(self, key: str, context: Dict[str, Any]):
        """Store context with timestamp"""
        self.context_store[key] = {
            "data": context,
            "timestamp": datetime.now().isoformat()
        }
        
    def get_context(self, key: str) -> Dict[str, Any]:
        """Retrieve context if exists, otherwise return empty dict"""
        context_data = self.context_store.get(key)
        if context_data is None:
            return {}
        return context_data.get("data", {})
        
    def add_vectors(self, vectors: np.ndarray, metadata: List[Dict[str, Any]]):
        """Add vectors with metadata to the index"""
        if vectors.shape[1] != self.vector_size:
            raise ValueError(f"Expected vector size {self.vector_size}, got {vectors.shape[1]}")
        
        start_idx = len(self.vector_metadata)
        self.vector_index.add(vectors)
        
        # Store metadata with vector IDs
        for i, meta in enumerate(metadata, start=start_idx):
            self.vector_metadata.append({
                "id": i,
                "metadata": meta,
                "timestamp": datetime.now().isoformat()
            })
    
    def search_vectors(self, query_vector: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar vectors and return their metadata"""
        if query_vector.shape[1] != self.vector_size:
            raise ValueError(f"Expected vector size {self.vector_size}, got {query_vector.shape[1]}")
        
        # Search for similar vectors
        distances, indices = self.vector_index.search(query_vector, k)
        
        # Return results with metadata
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.vector_metadata):
                result = {
                    "similarity_score": float(1 / (1 + dist)),  # Convert distance to similarity
                    "metadata": self.vector_metadata[idx]["metadata"],
                    "vector_id": int(idx)
                }
                results.append(result)
        
        return results
    
    def clear_old_contexts(self, max_age_hours: int = 24):
        """Clear contexts older than specified hours"""
        now = datetime.now()
        to_delete = []
        
        for key, value in self.context_store.items():
            stored_time = datetime.fromisoformat(value["timestamp"])
            age = (now - stored_time).total_seconds() / 3600
            
            if age > max_age_hours:
                to_delete.append(key)
                
        for key in to_delete:
            del self.context_store[key]
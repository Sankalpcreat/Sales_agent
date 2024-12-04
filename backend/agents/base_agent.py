from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from core.shared_memory import SharedMemoryService
from models.ollama_request import OllamaApiClient

class BaseAgent(ABC):
    def __init__(self, shared_memory: SharedMemoryService, api_client: OllamaApiClient):
        self.shared_memory = shared_memory
        self.api_client = api_client
    
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()
    
    def store_context(self, key: str, context: Dict[str, Any]) -> None:
        self.shared_memory.store_context(key, context)
    
    def get_context(self, key: str) -> Optional[Dict[str, Any]]:
        return self.shared_memory.get_context(key)
    
    def add_vectors(self, vectors: List[List[float]], metadata: List[Dict[str, Any]]) -> None:
        self.shared_memory.add_vectors(vectors, metadata)
    
    def search_vectors(self, query_vector: List[float], k: int = 5) -> List[Dict[str, Any]]:
        return self.shared_memory.search_vectors(query_vector, k)
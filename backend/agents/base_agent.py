from abc import ABC, abstractmethod
from typing import Dict, Any
from core.shared_memory import SharedMemoryService
from models.ollama_request import OllamaApiClient

class BaseAgent(ABC):
    def __init__(self, shared_memory: SharedMemoryService, api_client: OllamaApiClient):
        self.shared_memory = shared_memory
        self.api_client = api_client
    
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main task"""
        pass
    
    def store_context(self, key: str, context: Dict[str, Any]):
        """Store context in shared memory"""
        self.shared_memory.store_context(key, context)
    
    def get_context(self, key: str) -> Dict[str, Any]:
        """Retrieve context from shared memory"""
        return self.shared_memory.get_context(key)
    
    def add_vectors(self, vectors, metadata):
        """Add vectors to shared memory"""
        self.shared_memory.add_vectors(vectors, metadata)
    
    def search_vectors(self, query_vector, k=5):
        """Search vectors in shared memory"""
        return self.shared_memory.search_vectors(query_vector, k)# backend/agents/base_agent.py
        from abc import ABC, abstractmethod
        from typing import Dict, Any
        from core.shared_memory import SharedMemoryService
        from models.ollama_request import OllamaApiClient
        
        class BaseAgent(ABC):
            def __init__(self, shared_memory: SharedMemoryService, api_client: OllamaApiClient):
                self.shared_memory = shared_memory
                self.api_client = api_client
            
            @abstractmethod
            def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
                """Execute the agent's main task"""
                pass
            
            def store_context(self, key: str, context: Dict[str, Any]):
                """Store context in shared memory"""
                self.shared_memory.store_context(key, context)
            
            def get_context(self, key: str) -> Dict[str, Any]:
                """Retrieve context from shared memory"""
                return self.shared_memory.get_context(key)
            
            def add_vectors(self, vectors, metadata):
                """Add vectors to shared memory"""
                self.shared_memory.add_vectors(vectors, metadata)
            
            def search_vectors(self, query_vector, k=5):
                """Search vectors in shared memory"""
                return self.shared_memory.search_vectors(query_vector, k)
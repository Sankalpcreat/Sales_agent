from datetime import datetime
from typing import Dict, Any
import numpy as np

from agents.base_agent import BaseAgent
from core.shared_memory import SharedMemoryService
from models.ollama_request import OllamaApiClient
from core.database import DatabaseService

class LeadSuggestionsAgent(BaseAgent):
    def __init__(self, shared_memory: SharedMemoryService, api_client: OllamaApiClient):
        super().__init__(shared_memory, api_client)
        self.db_service = DatabaseService()

    def _generate_suggestions_vector(self, suggestions: str) -> np.ndarray:
        return np.mean([np.fromstring(suggestions.encode('utf-8'), dtype=np.float32)], axis=0)

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            context = self.shared_memory.get_context('latest_meeting_summary') or {}
            meeting_summary = context.get('summary', '')
            meeting_transcript = context.get('transcript', '')
            requirements = input_data.get('requirements', '')

            lead_prompt = f"""
            Generate lead suggestions based on:
            Meeting Summary: {meeting_summary}
            Meeting Transcript: {meeting_transcript}
            Requirements: {requirements}
            """

            suggestions = self.api_client.query_model(lead_prompt)
            
            if not suggestions:
                return {"status": "error", "message": "Failed to generate leads"}
            
            suggestions_vector = self._generate_suggestions_vector(suggestions)
            
            suggestions_context = {
                "input_requirements": requirements,
                "suggestions": suggestions,
                "source": input_data.get('source', 'unknown'),
                "timestamp": datetime.now().isoformat()
            }
            
            self.shared_memory.store_context("latest_lead_suggestions", suggestions_context)
            
            lead_data = {
                "company_name": "Potential Leads",
                "industry": "Multiple",
                "source": input_data.get('source', 'unknown'),
                "opportunity_details": suggestions_context
            }
            lead_id = self.db_service.store_lead(lead_data, suggestions_vector)
            
            self.shared_memory.add_vectors(
                suggestions_vector.reshape(1, -1),
                [{"type": "lead_suggestions", "source": input_data.get('source', 'unknown'), "db_id": lead_id}]
            )
            
            return {
                "status": "success",
                "suggestions": suggestions,
                "lead_id": lead_id
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
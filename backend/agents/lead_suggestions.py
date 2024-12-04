import hashlib
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
        self.db_service = DatabaseService()  # Initialize database service

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Retrieve context from shared memory
            context = self.shared_memory.get_context('latest_meeting_summary')
            
            # Extract meeting summary and transcript
            meeting_summary = context.get('summary', '')
            meeting_transcript = context.get('transcript', '')
            
            # Prepare prompt for lead generation
            requirements = input_data.get('requirements', '')
            
            # Generate lead suggestions
            lead_prompt = f"""
            Based on the following meeting context and requirements, generate a detailed lead suggestions report.

            Meeting Summary:
            {meeting_summary}

            Meeting Transcript:
            {meeting_transcript}

            Additional Requirements:
            {requirements}

            Please provide a structured report with the following sections:
            1. Potential Lead Profiles (3-5 companies)
               For each company:
               - Company Name
               - Industry
               - Size Range
               - Current Pain Points
               - Why They're a Good Fit

            2. Opportunity Assessment
               For each company:
               - Estimated Deal Size
               - Conversion Probability
               - Priority Level (High/Medium/Low)

            3. Engagement Strategy
               For each company:
               - Recommended Approach
               - Key Decision Makers to Target
               - Value Proposition
               - Potential Objections and Responses

            Format the response as a clear, actionable report with specific company recommendations.
            """
            
            # Generate lead suggestions using Ollama
            suggestions = self.api_client.query_model(lead_prompt)
            
            if not suggestions or suggestions.strip() == "":
                return {
                    "status": "error",
                    "message": "Failed to generate lead suggestions"
                }
            
            # Create vector representation of suggestions
            suggestions_vector = self._generate_suggestions_vector(suggestions)
            
            # Store suggestions in shared memory
            suggestions_context = {
                "input_requirements": requirements,
                "suggestions": suggestions,
                "source": input_data.get('source', 'unknown'),
                "timestamp": datetime.now().isoformat()
            }
            self.shared_memory.store_context("latest_lead_suggestions", suggestions_context)
            
            # Store lead suggestions in database
            lead_data = {
                "company_name": "Potential Leads",  # You might want to parse this from suggestions
                "industry": "Multiple",
                "source": input_data.get('source', 'unknown'),
                "opportunity_details": suggestions_context
            }
            lead_id = self.db_service.store_lead(lead_data, suggestions_vector)
            
            # Add vector to shared memory
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
            print(f"Error in lead suggestions generation: {str(e)}")
            return {
                "status": "error",
                "message": f"Error generating lead suggestions: {str(e)}"
            }

    def _generate_suggestions_vector(self, suggestions: str) -> np.ndarray:
        """
        Generate a consistent 768-dimensional vector representation
        """
        try:
            # Use a deterministic method to generate a 768-dimensional vector
            # Create a hash of the suggestions
            hash_bytes = hashlib.md5(suggestions.encode()).digest()
            
            # Convert hash bytes to a numpy array of float32
            base_vector = np.frombuffer(hash_bytes, dtype=np.float32)
            
            # Repeat and truncate to ensure exactly 768 dimensions
            # Use np.tile to repeat the vector and then slice
            vector = np.tile(base_vector, (768 // len(base_vector) + 1))[:768]
            
            # Normalize the vector to unit length
            vector = vector / np.linalg.norm(vector)
            
            return vector
        
        except Exception as e:
            print(f"Vector generation error: {e}")
            # Return a zero vector of the correct size as a fallback
            return np.zeros(768, dtype=np.float32)

    def _fallback_vector(self, text: str) -> np.ndarray:
        """
        Create a simple fallback vector representation
        """
        # Implement a basic fallback vector generation if needed
        return np.zeros(768, dtype=np.float32)
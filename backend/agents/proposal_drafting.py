# backend/agents/proposal_drafting.py
from typing import Dict, Any
from datetime import datetime
from .base_agent import BaseAgent
from core.shared_memory import SharedMemoryService
from models.ollama_request import OllamaApiClient

class ProposalDraftingAgent(BaseAgent):
    def __init__(self, shared_memory: SharedMemoryService, api_client: OllamaApiClient):
        super().__init__(shared_memory, api_client)
    
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Draft a proposal based on the input requirements
        """
        try:
            # Retrieve contexts from shared memory
            lead_context = self.shared_memory.get_context('latest_lead_suggestions', {})
            meeting_context = self.shared_memory.get_context('latest_meeting_summary', {})
            
            # Extract relevant information
            lead_suggestions = lead_context.get('suggestions', '')
            meeting_summary = meeting_context.get('summary', '')
            
            # Prepare a concise prompt
            requirements = input_data.get('requirements', '')
            prompt = f"""Create a sales proposal with the following sections:

Client Requirements:
{requirements}

Context:
{meeting_summary[:300] if meeting_summary else 'No meeting context'}
{lead_suggestions[:300] if lead_suggestions else 'No lead analysis'}

Format:
1. Executive Summary
2. Solution Overview
3. Implementation Plan
4. Pricing & Timeline

Use markdown formatting."""
            
            # Generate proposal using Ollama
            proposal_draft = self.api_client.query_model(prompt)
            
            if not proposal_draft or proposal_draft.startswith("Error") or proposal_draft == "No response from model.":
                # Try with even simpler prompt
                fallback_prompt = f"""Create a brief sales proposal addressing:
{requirements}

Include: Features, Implementation, and Pricing."""
                proposal_draft = self.api_client.query_model(fallback_prompt)
            
            if not proposal_draft or proposal_draft.strip() == "":
                return {
                    "status": "error",
                    "message": "Failed to generate proposal"
                }
            
            # Store proposal in shared memory
            proposal_context = {
                'draft': proposal_draft,
                'requirements': requirements,
                'timestamp': datetime.now().isoformat()
            }
            self.shared_memory.store_context('latest_proposal_context', proposal_context)
            
            return {
                'status': 'success',
                'proposal': proposal_draft,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'based_on_meeting': bool(meeting_summary),
                    'based_on_leads': bool(lead_suggestions)
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error generating proposal: {str(e)}'
            }
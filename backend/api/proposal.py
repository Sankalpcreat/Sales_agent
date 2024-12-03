from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from agents.proposal_drafting import ProposalDraftingAgent
from models.ollama_request import OllamaApiClient

router = APIRouter()

ollama_api_client = OllamaApiClient()
proposal_agent = ProposalDraftingAgent(ollama_api_client)

class ProposalRequest(BaseModel):
    client_name: str = Field(..., min_length=1)
    requirements: str = Field(..., min_length=1)

    @field_validator('client_name', 'requirements')
    @classmethod
    def validate_string_fields(cls, v):
        if not isinstance(v, str):
            raise ValueError("Must be a string")
        return v

@router.post("/proposal")
async def generate_proposal(request: ProposalRequest):
    try:
        proposal = proposal_agent.generate_proposal(request.client_name, request.requirements)
        return {"proposal": proposal}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating proposal: {str(e)}")
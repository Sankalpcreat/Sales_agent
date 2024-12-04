from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from agents.lead_scoring import LeadScoringAgent
from models.ollama_request import OllamaApiClient

router = APIRouter()

ollama_api_client = OllamaApiClient()
lead_scoring_agent = LeadScoringAgent(ollama_api_client)

class Lead(BaseModel):
    name: str
    engagement: int = Field(..., ge=0, le=100)
    activity: int = Field(..., ge=0, le=100)

class LeadsRequest(BaseModel):
    leads: List[Lead]

"""
COMMENTED OUT - Not currently in use
@router.post("/score_leads")
async def score_leads(request: LeadsRequest):
    # Implementation commented out
    pass
"""
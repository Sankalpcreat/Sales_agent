from fastapi import APIRouter, HTTPException
from agents.lead_scoring import LeadScoringAgent
from models.ollama_request import OllamaApiClient

router=APIRouter()

ollama_api_client=OllamaApiClient()
lead_scoring_agent=LeadScoringAgent(ollama_api_client)

@router.post("/score_leads")
async def score_leads(leads:list):

    if not leads:
        raise HTTPException(status_code=400,detail="No leads provided.")
    
    try:
        scores=lead_scoring_agent.score_leads(leads)
        return {"scores":scores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scoring leads: {str(e)}")
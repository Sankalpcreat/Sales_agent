from fastapi import APIRouter, HTTPException
from agents.proposal_drafting import ProposalDraftingAgent
from models.ollama_request import OllamaApiClient

router=APIRouter()

ollama_api_client=OllamaApiClient()
proposal_agent=ProposalDraftingAgent(ollama_api_client)

@router.post("/proposal")
async def generate_proposal(client_name:str,requirements:str):
    
    if not client_name or not requirements:
        raise HTTPException(status_code=400,detail="Client name and requirements are required.")
    try:
        proposal=proposal_agent.generate_proposal(client_name,requirements)
        return {"proposal":proposal}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error generating proposal:{str(e)}")
    
from fastapi import APIRouter, HTTPException
from agents.lead_suggestions import LeadSuggestionsAgent
from core.vector_search import VectorSearchService
import numpy as np

router = APIRouter()


vector_search_service = VectorSearchService(vector_size=128)  
lead_suggestions_agent = LeadSuggestionsAgent(vector_search_service)

@router.post("/lead_suggestions")
async def suggest_similar_leads(query_vector: list, top_k: int = 5):
    
    if not query_vector or not isinstance(query_vector, list):
        raise HTTPException(status_code=400, detail="Invalid query vector provided.")
    
    try:
        query_vector_np = np.array([query_vector]) 
        recommendations = lead_suggestions_agent.recommend_similar_leads(query_vector=query_vector_np, top_k=top_k)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating lead suggestions: {str(e)}")
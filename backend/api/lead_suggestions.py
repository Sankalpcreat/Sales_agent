from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import numpy as np

router = APIRouter()

class LeadSuggestionsRequest(BaseModel):
    query_vector: Optional[List[float]] = None
    top_k: int = 5

@router.post("/lead_suggestions")
async def suggest_similar_leads(request: LeadSuggestionsRequest):
    if not request.query_vector:
        raise HTTPException(status_code=400, detail="No query vector provided")
    
    try:
        query_vector = np.array(request.query_vector[:128], dtype=np.float32).reshape(1, -1)
        
        recommendations = LeadSuggestionsAgent.recommend_similar_leads(
            query_vector=query_vector, 
            top_k=request.top_k
        )
        
        return {
            "recommendations": recommendations,
            "top_k": request.top_k
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
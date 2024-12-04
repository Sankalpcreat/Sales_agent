from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from agents.lead_suggestions import LeadSuggestionsAgent
from core.vector_search import VectorSearchService
import numpy as np
import logging

router = APIRouter()

vector_search_service = VectorSearchService(vector_size=128)  
lead_suggestions_agent = LeadSuggestionsAgent(vector_search_service)

class LeadSuggestionsRequest(BaseModel):
    query_vector: Optional[List[float]] = None
    top_k: int = Field(default=5, ge=1, le=20)

@router.post("/lead_suggestions")
async def suggest_similar_leads(request: LeadSuggestionsRequest):
    # Explicit checks matching the test expectations
    if request.query_vector is None:
        raise HTTPException(status_code=400, detail="No query vector provided.")
    
    if len(request.query_vector) == 0:
        raise HTTPException(status_code=400, detail="Empty query vector.")
    
    try:
        # Ensure vector is exactly 128 dimensions
        query_vector = request.query_vector[:128]
        if len(query_vector) < 128:
            query_vector.extend([0.0] * (128 - len(query_vector)))
        
        # Convert to numpy array
        query_vector_np = np.array(query_vector, dtype=np.float32).reshape(1, -1)
        
        # Get recommendations
        top_k = request.top_k or 5
        recommendations = lead_suggestions_agent.recommend_similar_leads(
            query_vector=query_vector_np, 
            top_k=top_k
        )
        
        return {
            "recommendations": recommendations,
            "query_vector_length": len(query_vector),
            "top_k": top_k
        }
    except Exception as e:
        # Log the full error for debugging
        logging.error(f"Lead suggestions error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating lead suggestions: {str(e)}"
        )
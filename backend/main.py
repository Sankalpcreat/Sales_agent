from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import summarize, lead_suggestions, proposal, score_leads, follow_up

app = FastAPI(
    title="Sales Agent API",
    description="AI-powered sales assistant API for meeting summaries, lead scoring, and follow-ups",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(summarize.router, prefix="/api", tags=["Meeting Summary"])
app.include_router(lead_suggestions.router, prefix="/api", tags=["Lead Suggestions"])
app.include_router(proposal.router, prefix="/api", tags=["Proposal"])
app.include_router(score_leads.router, prefix="/api", tags=["Lead Scoring"])
app.include_router(follow_up.router, prefix="/api", tags=["Follow Up"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Sales Agent API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "Healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

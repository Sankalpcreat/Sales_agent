from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import proposal, summarize, score_leads, lead_suggestions, follow_up

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(proposal.router, prefix="/api")
app.include_router(summarize.router, prefix="/api")
app.include_router(score_leads.router, prefix="/api")
app.include_router(lead_suggestions.router, prefix="/api")
app.include_router(follow_up.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Sales Assistant Backend"}

@app.get("/health")
def health_check():
    return {"status": "Healthy"}

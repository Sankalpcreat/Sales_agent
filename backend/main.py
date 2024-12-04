# backend/main.py
import os
from fastapi import FastAPI, UploadFile, File
from core.shared_memory import SharedMemoryService
from core.orchestrator import CentralOrchestrator, TaskType
from models.ollama_request import OllamaApiClient
from models.transcription import TranscriptionService
from agents.meeting_summary import MeetingSummaryAgent
from agents.lead_suggestions import LeadSuggestionsAgent

# Determine Vosk model path
VOSK_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'vosk_model')

# Initialize shared services
shared_memory = SharedMemoryService(vector_size=768)
ollama_client = OllamaApiClient()
transcription_service = TranscriptionService(model_path=VOSK_MODEL_PATH)

# Initialize agents
meeting_agent = MeetingSummaryAgent(shared_memory, ollama_client, transcription_service)
lead_agent = LeadSuggestionsAgent(shared_memory, ollama_client)

# Initialize orchestrator
orchestrator = CentralOrchestrator()
orchestrator.agents[TaskType.MEETING_SUMMARY] = meeting_agent
orchestrator.agents[TaskType.LEAD_RECOMMENDATION] = lead_agent

# FastAPI setup
app = FastAPI()

@app.post("/process-meeting")
async def process_meeting(audio_file: UploadFile = File(...)):
    try:
        result = orchestrator.execute_task({
            "audio_path": audio_file.filename,
            "task": TaskType.MEETING_SUMMARY
        })
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/get-lead-suggestions")
async def get_lead_suggestions(requirements: str):
    try:
        result = orchestrator.execute_task({
            "requirements": requirements,
            "task": TaskType.LEAD_RECOMMENDATION
        })
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}
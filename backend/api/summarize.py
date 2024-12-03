import os
from fastapi import APIRouter, HTTPException, UploadFile
from agents.meeting_summary import MeetingSummaryAgent
from models.transcription import TranscriptionService
from models.ollama_request import OllamaApiClient

router = APIRouter()
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "vosk_model")


transcription_service = TranscriptionService(model_path=model_path)
ollama_api_client = OllamaApiClient()
summary_agent = MeetingSummaryAgent(transcription_service, ollama_api_client)

@router.post("/summarize")
async def summarize_meeting(file: UploadFile):
    
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")
    
    try:
       
        os.makedirs("temp", exist_ok=True)
        file_path = f"temp/{file.filename}"
        
        
        with open(file_path, "wb") as f:
            f.write(await file.read())

        
        summary = summary_agent.summarize_meeting(file_path)
        
        
        os.remove(file_path)
        
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing meeting: {str(e)}")

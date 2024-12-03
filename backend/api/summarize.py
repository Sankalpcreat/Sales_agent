import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from agents.meeting_summary import MeetingSummaryAgent
from models.transcription import TranscriptionService
from models.ollama_request import OllamaApiClient

router = APIRouter()
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "vosk_model")

transcription_service = TranscriptionService(model_path=model_path)
ollama_api_client = OllamaApiClient()
summary_agent = MeetingSummaryAgent(transcription_service, ollama_api_client)

@router.post("/summarize")
async def summarize_meeting(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")
    
    if not file.filename.lower().endswith('.wav'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only WAV files are supported.")
    
    try:
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded.")
        
        os.makedirs("temp", exist_ok=True)
        file_path = f"temp/{file.filename}"
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        try:
            summary = summary_agent.summarize_meeting(file_path)
            if summary.startswith("Error during transcription:"):
                error_msg = summary.replace("Error during transcription:", "").strip()
                raise HTTPException(status_code=400, detail=f"Transcription error: {error_msg}")
            return {"summary": summary}
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing meeting: {str(e)}")

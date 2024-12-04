from typing import Dict, Any
import os
import hashlib
import numpy as np

from .base_agent import BaseAgent
from models.transcription import TranscriptionService
from core.shared_memory import SharedMemoryService
from models.ollama_request import OllamaApiClient

class MeetingSummaryAgent(BaseAgent):
    def __init__(self, shared_memory: SharedMemoryService, 
                 api_client: OllamaApiClient, 
                 transcription_service: TranscriptionService):
        super().__init__(shared_memory, api_client)
        self.transcription_service = transcription_service
    
    def _generate_summary_vector(self, summary: str) -> np.ndarray:
        hash_bytes = hashlib.md5(summary.encode()).digest()
        return np.frombuffer(hash_bytes, dtype=np.float32)[:10] / 255.0

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            audio_path = input_data.get('audio_path', '')
            if not audio_path or not os.path.exists(audio_path):
                return {"status": "error", "message": "Invalid audio path"}
            
            transcript = self.transcription_service.transcribe(audio_path)
            
            if not transcript:
                return {"status": "error", "message": "No transcript generated"}
            
            summary_prompt = f"Summarize this meeting transcript: {transcript}"
            summary = self.api_client.query_model(summary_prompt)
            
            summary_vector = self._generate_summary_vector(summary)
            
            summary_context = {
                "transcript": transcript,
                "summary": summary,
                "source": input_data.get('source', 'unknown')
            }
            
            self.shared_memory.store_context("latest_meeting_summary", summary_context)
            
            self.shared_memory.add_vectors(
                summary_vector.reshape(1, -1),
                [{"type": "meeting_summary", "source": input_data.get('source', 'unknown')}]
            )
            
            return {
                "status": "success",
                "transcript": transcript,
                "summary": summary
            }
        
        except Exception as e:
            return {
                "status": "error", 
                "message": str(e)
            }
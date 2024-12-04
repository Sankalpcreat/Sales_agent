# backend/agents/meeting_summary.py
from typing import Dict, Any
import os
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
        """
        Generate a vector representation of the summary
        Fallback to a simple text-based vector if Ollama fails
        """
        try:
            # Try to get vector from Ollama
            vector_prompt = f"Generate a vector representation of this summary: {summary}"
            vector_str = self.api_client.query_model(vector_prompt)
            
            # Parse vector string to numpy array
            vector_str = vector_str.split('[')[-1].split(']')[0]
            vector = np.fromstring(vector_str, sep=',')
            
            # Ensure consistent vector size
            return vector if len(vector) > 0 else self._fallback_vector(summary)
        except Exception as e:
            print(f"Vector generation error: {e}")
            return self._fallback_vector(summary)
    
    def _fallback_vector(self, text: str) -> np.ndarray:
        """
        Create a simple fallback vector representation
        """
        # Use a simple hash-based approach
        import hashlib
        hash_bytes = hashlib.md5(text.encode()).digest()
        return np.frombuffer(hash_bytes, dtype=np.float32)[:10] / 255.0
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Validate audio path
            audio_path = input_data.get('audio_path', '')
            if not audio_path:
                return {
                    "status": "error",
                    "message": "No audio path provided"
                }
            
            # Check if file exists
            if not os.path.exists(audio_path):
                # Try to find file in the same directory as the script
                script_dir = os.path.dirname(os.path.abspath(__file__))
                audio_path = os.path.join(script_dir, '..', audio_path)
                
                if not os.path.exists(audio_path):
                    return {
                        "status": "error",
                        "message": f"Audio file not found: {audio_path}"
                    }
            
            # Transcribe audio
            transcript = self.transcription_service.transcribe(audio_path)
            
            # Handle empty transcript
            if not transcript:
                return {
                    "status": "error",
                    "message": "No transcript generated"
                }
            
            # Generate structured summary using Ollama
            summary_prompt = f"""
            Analyze the following meeting transcript and provide a structured summary:

            Transcript:
            {transcript}

            Please provide a summary with the following sections:
            1. Meeting Overview
            2. Key Participants
            3. Discussion Points
            4. Action Items
            5. Next Steps
            6. Potential Opportunities

            Format the response as a clear, professional summary that highlights the most important aspects of the meeting.
            """
            
            summary = self.api_client.query_model(summary_prompt)
            
            # Create vector representation of summary
            summary_vector = self._generate_summary_vector(summary)
            
            # Store summary and vector in shared memory
            summary_context = {
                "transcript": transcript,
                "summary": summary,
                "source": input_data.get('source', 'unknown')
            }
            self.store_context("latest_meeting_summary", summary_context)
            
            # Add vector to shared memory
            self.add_vectors(summary_vector, [{"type": "meeting_summary", "source": input_data.get('source', 'unknown')}])
            
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
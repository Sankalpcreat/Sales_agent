from models.transcription import TranscriptionService
from models.ollama_request import OllamaApiClient

class MeetingSummaryAgent:

    def __init__(self,transcription_service:TranscriptionService,api_client:OllamaApiClient):

        self.transcription_service=transcription_service
        self.api_client=api_client
    
    def summarize_meeting(self,audio_file:str)->str:

        transcript=self.transcription_service.transcribe(audio_file)

        if "Error during transcription" in transcript:
            return transcript
        
        prompt=(
            f"Summarize the following meeting transcript:\n{transcript}\n"
            "Please provide a clear and concise summary."
        )
        summary=self.api_client.query_model(prompt)
        return summary
        
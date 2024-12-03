from models.transcription import TranscriptionService
from models.ollama_request import OllamaApiClient

class MeetingSummaryAgent:

    def __init__(self,transcription_service:TranscriptionService,api_client:OllamaApiClient):

        self.transcription_service=transcription_service
        self.api_client=api_client
    
    def summarize_meeting(self,audio_file:str)->str:
        print(f"Processing audio file: {audio_file}")
        
        transcript=self.transcription_service.transcribe(audio_file)
        print(f"Transcription result: {transcript}")

        if "Error during transcription" in transcript:
            print(f"Transcription error detected: {transcript}")
            return transcript
        
        if not transcript.strip():
            print("Empty transcript received")
            return "Error: No speech content was detected in the audio file"
        
        prompt=(
            f"Below is a complete transcript from an audio recording. Please summarize its content, no matter how brief it may be:\n\n"
            f"TRANSCRIPT:\n{transcript}\n\n"
            f"SUMMARY:"
        )
        print(f"Sending prompt to model: {prompt}")
        
        summary=self.api_client.query_model(prompt)
        print(f"Received summary: {summary}")
        return summary
        
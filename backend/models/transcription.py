import json
import wave
from typing import Optional
from vosk import Model, KaldiRecognizer

class TranscriptionService:
    def __init__(self, model_path: str):
        self.model = Model(model_path)

    def transcribe(self, audio_file: str) -> str:
        try:
            with wave.open(audio_file, "rb") as wf:
                
                if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
                    raise ValueError("Audio must be mono PCM WAV format")

                recognizer = KaldiRecognizer(self.model, wf.getframerate())
                transcription = []

                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        text = result.get('text', '').strip()
                        if text:
                            transcription.append(text)

                
                final_result = json.loads(recognizer.FinalResult())
                final_text = final_result.get('text', '').strip()
                if final_text:
                    transcription.append(final_text)

                return ' '.join(transcription).strip()
        
        except Exception as e:
            return f"Transcription error: {str(e)}"
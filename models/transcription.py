import json
import wave
from vosk import Model, KaldiRecognizer

class TranscriptionService:
    def __init__(self, model_path: str):
        self.model = Model(model_path)

    def transcribe(self, audio_file: str) -> str:
        try:
            with wave.open(audio_file, "rb") as wf:
                if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                    raise ValueError("Audio file must be mono PCM WAV format.")

                recognizer = KaldiRecognizer(self.model, wf.getframerate())
                transcription = []

                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        transcription.append(result.get('text', ''))

                final_result = json.loads(recognizer.FinalResult())
                transcription.append(final_result.get('text', ''))

                return ' '.join(transcription).strip()
        except Exception as e:
            return f"Error during transcription: {e}"

import json
import wave
from vosk import Model, KaldiRecognizer

class TranscriptionService:
    def __init__(self, model_path: str):
        self.model = Model(model_path)

    def transcribe(self, audio_file: str) -> str:
        try:
            print(f"Opening audio file: {audio_file}")
            with wave.open(audio_file, "rb") as wf:
                print(f"Audio file details:")
                print(f"- Channels: {wf.getnchannels()}")
                print(f"- Sample width: {wf.getsampwidth()}")
                print(f"- Frame rate: {wf.getframerate()}")
                print(f"- Compression type: {wf.getcomptype()}")
                
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
                        text = result.get('text', '')
                        if text:
                            print(f"Recognized text: {text}")
                            transcription.append(text)

                final_result = json.loads(recognizer.FinalResult())
                final_text = final_result.get('text', '')
                if final_text:
                    print(f"Final recognition: {final_text}")
                    transcription.append(final_text)

                full_text = ' '.join(transcription).strip()
                print(f"Complete transcription: {full_text}")
                return full_text
                
        except Exception as e:
            error_msg = f"Error during transcription: {e}"
            print(error_msg)
            return error_msg

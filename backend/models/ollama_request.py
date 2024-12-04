import requests
import time
from typing import Optional

class OllamaApiClient:
    def __init__(self, api_url: str = "http://localhost:11434/api/generate"):
        self.api_url = api_url
        self.max_retries = 3
        self.base_delay = 2

    def query_model(self, prompt: str, model: str = "llama3.2:latest") -> str:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(self.api_url, json=payload, timeout=30)
                response.raise_for_status()
                return response.json().get('response', '').strip()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(self.base_delay * (attempt + 1))

        return ''
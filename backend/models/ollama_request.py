import requests

class OllamaApiClient:

    def __init__(self,api_url:str="http://localhost:11434/api/generate"):
        self.api_url=api_url
        self.max_retries = 3
        self.base_delay = 2  # Base delay in seconds
    
    def query_model(self,prompt:str,model:str="llama3.2:latest")->str:
        payload={
            "model": model,
            "prompt": prompt,
            "stream": False  
        }
        for attempt in range(self.max_retries):
            try:
                response=requests.post(self.api_url,json=payload,timeout=60)
                response.raise_for_status()
                
                response_data = response.json()
                if not response_data.get("response"):
                    return "No response from model."
                return response_data["response"]
                
            except requests.exceptions.RequestException as e:
                if "rate limit exceeded" in str(e).lower():
                    if attempt < self.max_retries - 1:
                        delay = self.base_delay * (2 ** attempt)  # Exponential backoff
                        import time
                        time.sleep(delay)
                        continue
                return f"Error querying model: {e}"
            except ValueError as e:
                return f"Error parsing model response: {e}"
        
        return "Failed after maximum retries"

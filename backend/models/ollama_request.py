import requests

class OllamaApiClient:

    def __init__(self,api_url:str="http://localhost:11434/api/generate"):
        self.api_url=api_url
    
    def query_model(self,prompt:str,model:str="llama3.2:latest")->str:
        payload={
            "model": model,
            "prompt": prompt,
            "stream": False  # Explicitly disable streaming
        }
        try:
            response=requests.post(self.api_url,json=payload,timeout=30)
            response.raise_for_status()
            
            response_data = response.json()
            if not response_data.get("response"):
                return "No response from model."
            return response_data["response"]
            
        except requests.exceptions.RequestException as e:
            return f"Error querying model: {e}"
        except ValueError as e:
            return f"Error parsing model response: {e}"

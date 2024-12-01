import requests

class OllamaApiClient:

    def __init__(self,api_url:str="http://localhost:11400/api/generate"):
        self.api_url=api_url
    
    def query_model(self,prompt:str,model:str="llama3.2:latest")->str:

        payload={"model":model,"prompt":prompt}
        try:
            response=requests.post(self.api_url,json=payload,timeout=10)
            response.raise_for_status()
            return response.json().get("response","No response from model.")
        except requests.exceptions.RequestException as e:
            return f"Error querying model: {e}"


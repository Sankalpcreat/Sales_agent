from models.ollama_request import OllamaApiClient

class ProposalDraftingAgent:
    def __init__(self,api_client:OllamaApiClient):
        self.api_client=api_client

    def generate_proposal(self,client_name:str,requirements:str)->str:
        prompt=(
            f"Draft a proposal for the following client:\n"
            f"Client Name:{client_name}\n"
            f"Requirements:{requirements}\n"
            f"Please provide a professional and detailed proposal."
        )
        response=self.api_client.query_model(prompt)
        return response
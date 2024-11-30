from models.ollama_request import OllamaApiClient

class LeadScoringAgent:
    def __init__(self, ollama_client: OllamaApiClient):
       
        self.ollama_client = ollama_client

    def score_leads(self, leads: list) -> list:
        
        scored_leads = []
        for lead in leads:
            prompt = (
                f"Score the following lead based on engagement and activity:\n"
                f"Name: {lead['name']}, Engagement: {lead['engagement']}, Activity: {lead['activity']}"
            )
            score = self.ollama_client.query_model(prompt)
            scored_leads.append({"name": lead["name"], "score": score})
        return scored_leads

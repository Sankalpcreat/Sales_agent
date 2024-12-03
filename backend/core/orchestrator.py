class Orchestrator:
    def __init__(self):
        self.agent = {}

    def register_agent(self, name: str, agent):
        self.agent[name] = agent

    def execute_workflow(self, workflow_name: str, data: dict):
        if workflow_name not in self.agent:
            raise ValueError(f"Workflow {workflow_name} not registered.")
        try:
            result = self.agent[workflow_name](data)
            return result
        except Exception as e:
            return f"Error executing workflow '{workflow_name}': {e}"
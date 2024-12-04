from enum import Enum, auto
from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent

class TaskType(Enum):
    MEETING_SUMMARY = auto()
    LEAD_RECOMMENDATION = auto()

class CentralOrchestrator:
    def __init__(self):
        self.agents: Dict[TaskType, Optional[BaseAgent]] = {}

    def execute_task(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        task = input_data.get('task')
        agent = self.agents.get(task)

        if not agent:
            return {"status": "error", "message": f"No agent for task {task}"}

        try:
            return agent.execute(input_data)
        except Exception as e:
            return {"status": "error", "message": str(e)}
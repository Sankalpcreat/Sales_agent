# backend/core/orchestrator.py
from typing import Dict, Any
from enum import Enum
import logging
from datetime import datetime
from .vector_search import VectorSearchService
from .database import DatabaseService

class TaskType(Enum):
    LEAD_SCORING = "lead_scoring"
    MEETING_SUMMARY = "meeting_summary"
    PROPOSAL_DRAFTING = "proposal_drafting"
    LEAD_RECOMMENDATION = "lead_recommendation"

class CentralOrchestrator:
    def __init__(self):
        self.agents = {}
        self.vector_db = VectorSearchService(vector_size=768)  # or your chosen size
        
        # Initialize database service with fallback
        try:
            self.db = DatabaseService()
        except Exception as e:
            logging.warning(f"Database service initialization failed: {e}")
            self.db = None
        
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("Orchestrator")
    
    def determine_task_type(self, input_data: Dict[str, Any]) -> TaskType:
        # Check for explicitly specified task type
        if 'task' in input_data:
            return input_data['task']
        
        # Determine task type based on input content
        if "audio" in input_data:
            return TaskType.MEETING_SUMMARY
        elif "lead_info" in input_data:
            return TaskType.LEAD_SCORING
        elif "requirements" in input_data:
            # Check if requirements are for lead recommendation or proposal drafting
            requirements = input_data.get('requirements', '').lower()
            if any(keyword in requirements for keyword in ['proposal', 'draft', 'document']):
                return TaskType.PROPOSAL_DRAFTING
            return TaskType.LEAD_RECOMMENDATION
        
        # Default fallback
        return TaskType.PROPOSAL_DRAFTING
    
    def execute_task(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Determine task type
            task_type = self.determine_task_type(input_data)
            self.logger.info(f"Executing task: {task_type}")
            
            # Execute appropriate agent
            agent = self.agents.get(task_type)
            if not agent:
                raise ValueError(f"No agent registered for {task_type}")
            
            # Execute and log result
            result = agent.execute(input_data)
            self.logger.info(f"Task completed: {task_type}")
            
            return {
                "status": "success",
                "task_type": task_type.value,
                "result": result,
                "metadata": {
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Task execution failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "metadata": {
                    "timestamp": datetime.now().isoformat()
                }
            }
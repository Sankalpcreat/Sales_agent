from fastapi import APIRouter, HTTPException
from agents.follow_up import FollowUpAgent
from core.scheduler import SchedulerService
from pydantic import BaseModel
from datetime import datetime

class FollowUpRequest(BaseModel):
    lead_id: int
    follow_up_time: str
    message: str

router = APIRouter()

scheduler_service = SchedulerService()
follow_up_agent = FollowUpAgent(scheduler_service)

"""
COMMENTED OUT - Not currently in use
@router.post("/follow_up")
async def schedule_follow_up(request: FollowUpRequest):
    try:
        # Validate date format
        try:
            datetime.strptime(request.follow_up_time, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid date format")

        follow_up_agent.schedule_follow_up(
            request.lead_id,
            request.follow_up_time,
            request.message
        )
        return {"message": "Follow-up scheduled successfully."}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scheduling follow-up: {str(e)}")
"""
from fastapi import APIRouter, HTTPException
from agents.follow_up import FollowUpAgent
from core.scheduler import SchedulerService

router=APIRouter()

scheduler_service=SchedulerService()
follow_up_agent=FollowUpAgent(scheduler_service)

@router.post("/follow_up")
async def schedule_follow_up(lead_id:int,follow_up_time:str,message:str):

    if not lead_id or not follow_up_time or not message:
        raise HTTPException(status_code=400,detail="Missing required parameters.")

    try:
        follow_up_agent.schedule_follow_up(lead_id,follow_up_time,message)
        return {"message":"Follow-up scheduled successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scheduling follow-up: {str(e)}")
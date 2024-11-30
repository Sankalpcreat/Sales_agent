from core.scheduler import SchedulerService
from core.database import connect_to_database

class FollowUpAgent:

    def __init__(self,scheduler_service:SchedulerService):
        self.scheduler_service=scheduler_service
    
    def schedule_follow_up(self,lead_id:int,follow_up_time:str,message:str):

        def follow_up_task():
            conn = connect_to_database()
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO follow_ups (lead_id, message, status) VALUES (%s, %s, %s)",
                    (lead_id, message, "Scheduled"),
                )
                conn.commit()

        self.scheduler_service.add_job(follow_up_task, trigger="date", run_date=follow_up_time)       
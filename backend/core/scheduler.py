"""
COMMENTED OUT - Not currently in use
from apscheduler.schedulers.background import BackgroundScheduler

class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
    
    def add_job(self, func, trigger: str, **kwargs):
        return self.scheduler.add_job(func=func, trigger=trigger, **kwargs)
    
    def start(self):
        self.scheduler.start()
        print("Scheduler started successfully!")
    
    def shutdown(self):
        self.scheduler.shutdown(wait=True)
        print("Scheduler shutdown successfully!")
"""
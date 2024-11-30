from apscheduler.schedulers.background import BackgroundScheduler

class SchedulerService:
    def __init__(self):
        self.scheduler=BackgroundScheduler()
    
    def add_job(self,func,trigger:str,**kwargs):
        self.scheduler.add_job(func,trigger,**kwargs)
    
    def start(self):
        self.scheduler.start()
        print("Scheduler started successfully!")
        
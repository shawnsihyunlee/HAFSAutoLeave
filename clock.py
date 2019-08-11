from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
import autoleavescript

q = Queue(connection=conn)

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='sun', hour=18, minute=13, timezone="Asia/Seoul")
def scheduled_job():
	#print("Test: Monday")
	autoleavescript.doSignup()
	#q.enqueue(test)
    #q.enqueue(irregularleavescript.doSignup)

# def test():
# 	print("This job is run by the worker every minute.")

sched.start()




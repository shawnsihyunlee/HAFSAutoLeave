from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
import irregularleavescript

q = Queue(connection=conn)

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def scheduled_job():
	print("Test 1 minute interval")
	#irregularleavescript.doSignup()
	#q.enqueue(test)
    #q.enqueue(irregularleavescript.doSignup)

# def test():
# 	print("This job is run by the worker every minute.")

sched.start()
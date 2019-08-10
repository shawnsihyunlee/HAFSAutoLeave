from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
import irregularleavescript

q = Queue(connection=conn)

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes='1')
def scheduled_job():
	print("This job is run every minute.")
    #q.enqueue(irregularleavescript.doSignup)



sched.start()
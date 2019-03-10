from queue import Queue
import time as time

def do_stuff(q):
	while not q.empty():
		print(q.get())
		q.task_done()
		time.sleep(1)

q = Queue(maxsize=0)

for x in range(20):
	q.put(["Name",x])

do_stuff(q)
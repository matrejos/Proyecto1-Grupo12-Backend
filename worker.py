import os
import redis
from rq import Worker, Queue, Connection
from execute import execute

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://:paae68fcffdf5a21a871316e17a55a294c1658d8a7de76ed97c7a4bfabe46f589@ec2-52-44-129-161.compute-1.amazonaws.com:17599')

conn = redis.from_url(redis_url)

queue = Queue(connection=conn)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        queue.enqueue(execute)
        worker.work()

from app.limiter import TokenBucket
import time

class Storage:
    def __init__(self):
        self.storage = {}

    def get_bucket(self, client_ip):
        if client_ip in self.storage:
            return self.storage[client_ip]
        else:
            bucket = TokenBucket(2,time.perf_counter())
            self.storage[client_ip] = bucket
            return bucket

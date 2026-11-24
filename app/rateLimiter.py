from app.storage import Storage
from app.redis_storage import RedisStorage

class RateLimiter:
    def __init__(self,storage):
        self.storage = storage

    def allow_request(self,client_ip):
        bucket = self.storage.get_bucket(client_ip)
        allowed =  bucket.consume()
        self.storage.save_bucket(client_ip,bucket)
        return allowed
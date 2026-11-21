from app.storage import Storage

class RateLimiter:
    def __init__(self,storage):
        self.storage = storage

    def allow_request(self,client_ip):
        bucket = self.storage.get_bucket(client_ip)
        return bucket.consume()
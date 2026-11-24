class RateLimiter:
    def __init__(self,storage):
        self.storage = storage

    def allow_request(self,client_ip):
        return self.storage.allow_request(client_ip)
from app.redis_client import redis_client
from app.limiter import TokenBucket
import time

class RedisStorage:
    def __init__(self):
        self.redis = redis_client

    def get_bucket(self, client_ip):
        bucket = self.redis.hgetall(f"rate_limit:{client_ip}")
        if not bucket:
            self.redis.hset(
                    f"rate_limit:{client_ip}",
                    mapping={
                        "capacity" : "2",
                        "tokens": "2",
                        "timestamp": f"{time.time()}"
                    }
                )
            bucket = self.redis.hgetall(f"rate_limit:{client_ip}")
        capacity = int(bucket["capacity"])
        token_count = float(bucket["tokens"])
        timestamp = float(bucket["timestamp"])
        return TokenBucket(capacity,token_count,timestamp)

    def save_bucket(self, client_ip, bucket):
        self.redis.hset(
            f"rate_limit:{client_ip}",
            mapping={
                "capacity": bucket.capacity,
                "tokens": bucket.token_count,
                "timestamp": bucket.timestamp
            }
        )
        
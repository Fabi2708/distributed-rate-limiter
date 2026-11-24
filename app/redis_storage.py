from app.redis_client import redis_client
from app.limiter import TokenBucket
import time
import os

class RedisStorage:
    def __init__(self):
        self.redis = redis_client
        script_path = os.path.join(
            os.path.dirname(__file__),
            "scripts",
            "token_bucket.lua"
        )

        with open(script_path, "r") as file:
            lua_script = file.read()

        self.allow_script = self.redis.register_script(lua_script)

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

    def allow_request(self,client_ip):
        redis_key = f"rate_limit:{client_ip}"

        result = self.allow_script(
            keys=[redis_key],
            client=self.redis
        )

        return bool(result)
        
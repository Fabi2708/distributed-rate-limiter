from app.redis_storage import RedisStorage
from app.redis_client import redis_client
import time

def test_ttl():
    storage = RedisStorage(ttl_seconds=5)
    client_ip = "192.168.1.10"
    redis_key = f"rate_limit:{client_ip}"
    redis_client.delete(redis_key)
    storage.allow_request(client_ip)
    assert redis_client.exists(redis_key) == 1
    time.sleep(6)
    assert redis_client.exists(redis_key) == 0
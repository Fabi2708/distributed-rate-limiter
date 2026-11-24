from app.redis_storage import RedisStorage
from app.redis_client import redis_client
import time

def test_allow_request():
    storage = RedisStorage()
    client_ip = "192.168.1.10"
    redis_key = f"rate_limit:{client_ip}"
    redis_client.delete(redis_key)
    assert storage.allow_request(client_ip) is True
    assert storage.allow_request(client_ip) is True
    assert storage.allow_request(client_ip) is False
    time.sleep(6)
    assert storage.allow_request(client_ip) is True
    redis_client.delete(redis_key)
from app.redis_client import redis_client

def test_redis_client():
    client_ip = "192.168.1.10"
    
    redis_client.hset(
        f"rate_limit:{client_ip}",
        mapping={
            "capacity" : "2",
            "tokens": "2",
            "timestamp": "1790000000"
        }
    )

    bucket = redis_client.hgetall(f"rate_limit:{client_ip}")
    assert bucket["capacity"] == "2"
    assert bucket["tokens"] == "2"
    assert bucket["timestamp"] == "1790000000"
    redis_client.delete(f"rate_limit:{client_ip}")
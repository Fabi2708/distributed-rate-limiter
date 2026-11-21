from app.rateLimiter import RateLimiter
from app.storage import Storage

def test_allow_requests():
    storage = Storage()
    rateLimiter = RateLimiter(storage)
    assert rateLimiter.allow_request("192.168.1.10") is True
    assert rateLimiter.allow_request("192.168.1.10") is True
    assert rateLimiter.allow_request("192.168.1.10") is False
    assert rateLimiter.allow_request("192.168.1.11") is True
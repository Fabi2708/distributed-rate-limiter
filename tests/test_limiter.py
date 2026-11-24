from test_main import client
from app.limiter import TokenBucket
import time

def test_consume_fail():
    bucket = TokenBucket(2,2,time.time())
    assert bucket.consume() is True
    assert bucket.consume() is True
    assert bucket.consume() is False

def test_consume_replenish():
    bucket= TokenBucket(1,1,time.time())
    assert bucket.consume() is True
    assert bucket.consume() is False
    bucket.timestamp = time.time() - 6
    assert bucket.consume() is True
from test_main import client
from app.limiter import TokenBucket
import time

def test_consume_fail():
    bucket = TokenBucket(2,time.perf_counter())
    assert bucket.consume() is True
    assert bucket.consume() is True
    assert bucket.consume() is False

def test_consume_replenish():
    bucket= TokenBucket(1,time.perf_counter())
    assert bucket.consume() is True
    assert bucket.consume() is False
    bucket.timestamp = time.perf_counter() - 6
    assert bucket.consume() is True
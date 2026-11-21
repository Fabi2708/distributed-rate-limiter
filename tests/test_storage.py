from app.storage import Storage

def test_get_bucket_same():
    client_ip = "192.168.1.10"
    storage = Storage()
    bucket1 = storage.get_bucket(client_ip)
    bucket2 = storage.get_bucket(client_ip)
    assert bucket1 is bucket2

def test_get_bucket_different():
    storage = Storage()
    bucket1 = storage.get_bucket("192.168.1.11")
    bucket2 = storage.get_bucket("192.168.1.12")
    assert bucket1 is not bucket2
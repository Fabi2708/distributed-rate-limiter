from test_main import client

def test_api():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Rate Limiter API"
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Rate Limiter API"
    response = client.get("/")
    assert response.status_code == 429
    assert response.json()["detail"] == "Too many requests!"
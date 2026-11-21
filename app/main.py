from fastapi import FastAPI, Request, HTTPException
from app.rateLimiter import RateLimiter
from app.storage import Storage

storage = Storage()
rate_limiter = RateLimiter(storage)
app = FastAPI()

@app.get("/")
async def hello(request: Request):
    client_host = request.client.host
    if rate_limiter.allow_request(client_host):
        return {"message": "Rate Limiter API"}
    else:
        raise HTTPException(status_code=429,detail="Too many requests!")

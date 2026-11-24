from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.rateLimiter import RateLimiter
from app.storage import Storage
from app.redis_storage import RedisStorage

storage = RedisStorage()
rate_limiter = RateLimiter(storage)
app = FastAPI()

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client_host = request.client.host
    if not rate_limiter.allow_request(client_host):
        return JSONResponse(status_code=429, content={"detail": "Too many requests!"})
    return await call_next(request)

@app.get("/")
async def hello(request: Request):
    return {"message": "Rate Limiter API"}


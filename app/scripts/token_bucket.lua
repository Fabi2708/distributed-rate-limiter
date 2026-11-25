local time = redis.call("TIME")
local current_time = tonumber(time[1]) + tonumber(time[2]) / 1000000

if redis.call("EXISTS", KEYS[1]) == 0 then
    redis.call("HSET",KEYS[1],
        "capacity", 2,
        "tokens", 2,
        "timestamp", current_time
    )
end

local tokens = tonumber(redis.call("HGET", KEYS[1], "tokens"))
local capacity = tonumber(redis.call("HGET", KEYS[1], "capacity"))
local timestamp = tonumber(redis.call("HGET", KEYS[1], "timestamp"))


local elapsed_time = current_time - timestamp

local refill_rate = 10/60
local tokens_to_add = elapsed_time * refill_rate
local new_tokens = math.min(tokens + tokens_to_add, capacity)

local allowed = 0
if new_tokens >= 1 then
    new_tokens = new_tokens - 1
    allowed = 1
end

redis.call(
    "HSET", KEYS[1],
    "tokens", new_tokens,
    "timestamp", current_time
)

redis.call("EXPIRE", KEYS[1], tonumber(ARGV[1]))

return allowed
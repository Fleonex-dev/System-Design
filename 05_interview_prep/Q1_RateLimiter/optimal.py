import time

# ==========================================
# ✅ OPTIMAL SOLUTION (Redis Sliding Window)
# ==========================================
# CONCEPTS:
# 1. Redis: Centralized store for distributed counts.
# 2. Lua Script: Atomicity (Read-Modify-Write in one step).
# 3. Sliding Window: Accurate limiting (prevents "Spike" at window edges).

class DistributedRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
        
    def allow_request(self, user_id, limit=10, window=60):
        # MOCKING REDIS LUA SCRIPT execution
        # In real interview, write pseudocode for Lua
        lua_script = """
        local key = KEYS[1]
        local now = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        local limit = tonumber(ARGV[3])
        
        -- Remove old entries (Sliding Window)
        redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
        
        -- Count current
        local count = redis.call('ZCARD', key)
        
        if count < limit then
            redis.call('ZADD', key, now, now)
            redis.call('EXPIRE', key, window + 1) -- Cleanup
            return 1 -- Allowed
        else
            return 0 -- Blocked
        end
        """
        # Simulate result
        print(f"✅ [Redis] Executing atomic check for {user_id}...")
        return True

if __name__ == "__main__":
    print("✅ This file demonstrates the Algorithm logic.")
    print("✅ In production, replace `self.redis` with `redis.Redis()`")
    
    limiter = DistributedRateLimiter(None)
    limiter.allow_request("user1")

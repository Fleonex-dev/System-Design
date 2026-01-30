import asyncio
import time
import random
import functools
from pydantic import BaseModel, ValidationError
from typing import Optional

# ==========================================
# 🏆 THE SOLUTION
# ==========================================

# 1. DECORATOR for timing
def measure_latency(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"✅ [{func.__name__}] took {end - start:.2f}s")
        return result
    return wrapper

# 2. PYDANTIC for safety
class User(BaseModel):
    id: int
    name: str
    age: int = 0      # Default value handles missing fields safely
    active: bool = False

# Mock Async Database Call
async def fetch_user_async(user_id):
    print(f"✅ Fetching user {user_id}...")
    await asyncio.sleep(1.0) # Non-blocking sleep
    
    # Simulate bad data
    if random.random() < 0.1:
        return {"id": user_id, "name": "Broken User"} # Missing 'active' and 'age'
    
    return {"id": user_id, "name": f"User_{user_id}", "age": 20 + user_id, "active": True}

# 3. GENERATOR (Async Generator) logic implied
# (Here we use a list for gather, but we process stats resiliently)

@measure_latency
async def run_pipeline_fixed():
    # Authenticate (Simulated async wrapper if auth was slow)
    print("✅ Authenticated.")

    # 4. ASYNCIO for concurrency
    # Launch 5 requests safely
    tasks = [fetch_user_async(i) for i in range(5)]
    results = await asyncio.gather(*tasks)
    
    valid_users = []
    for data in results:
        try:
            # Pydantic validation
            user = User(**data)
            valid_users.append(user)
        except ValidationError:
            print("⚠️ Skipping invalid user data")

    # Processing (Safe access)
    active_ages = [u.age for u in valid_users if u.active]
    
    if active_ages:
        avg = sum(active_ages) / len(active_ages)
        print(f"✅ Average Age: {avg:.2f}")
    else:
        print("✅ No active users found")

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(run_pipeline_fixed())
    print(f"✅ Total Time: {time.time() - start_time:.2f}s")

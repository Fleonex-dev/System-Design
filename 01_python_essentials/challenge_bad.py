import time
import random

# ==========================================
# 💀 THE CHALLENGE: FIX THIS TRASH CODE
# ==========================================
# SCENARIO: 
# You inherited this code from a developer who was fired.
# It processes user data from a "Legacy API".
# 
# PROBLEMS:
# 1. It's SEQUENTIAL (Sync). Fetching 5 users takes 5 seconds. It should take ~1s.
# 2. It uses raw DICTS. If a field is missing, it crashes.
# 3. It loads ALL users into a list before processing. Memory hog.
# 4. Calibration logic is copy-pasted (Boilerplate).
# 
# GOAL:
# Refactor this into `challenge_solution.py` using:
# - Asyncio (for fetching)
# - Pydantic (for validation)
# - Generators (for processing stats)
# - Decorators (for timing authentication)

def authenticate():
    print("💀 Authenticating...")
    time.sleep(0.5)
    print("💀 Authenticated.")

def fetch_user_from_db(user_id):
    print(f"💀 Fetching user {user_id}...")
    time.sleep(1.0) # Network delay
    
    # 10% chance of returning bad data (missing fields)
    if random.random() < 0.1:
        return {"id": user_id, "name": "Broken User"}
    
    return {"id": user_id, "name": f"User_{user_id}", "age": 20 + user_id, "active": True}

def run_pipeline():
    start_time = time.time()
    
    authenticate()
    
    # PROBLEM 1: This blocks.
    users = []
    for i in range(5):
        users.append(fetch_user_from_db(i))
        
    # PROBLEM 2: What if 'age' is missing? Crash.
    total_age = 0
    for u in users:
        if u['active']: # PROBLEM 3: Unsafe access
            total_age += u['age']
            
    print(f"💀 Average Age: {total_age / len(users)}")
    print(f"💀 Total Time: {time.time() - start_time:.2f}s (Should be < 1.5s)")

if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        print(f"\n💥 CRITICAL FAILURE: {e}")

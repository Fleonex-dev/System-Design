import time

# ==========================================
# 🛑 BAD SOLUTION (In-Memory Fixed Window)
# ==========================================
# PROBLEMS:
# 1. Not Distributed: If you have 2 servers, user can hit 2x limit.
# 2. Race Conditions: No locking.
# 3. Memory Leak: We never clean up old timestamps.

rate_limit_map = {}

def allow_request(user_id):
    current_window = int(time.time()) # Per second window
    key = f"{user_id}:{current_window}"
    
    # PROBLEM 3: Map grows infinitely with new windows
    if key not in rate_limit_map:
        rate_limit_map[key] = 0
        
    if rate_limit_map[key] < 10:
        rate_limit_map[key] += 1
        return True
    return False

if __name__ == "__main__":
    print("🛑 Running Bad Rate Limiter...")
    for i in range(15):
        print(f"Req {i}: {allow_request('user1')}")

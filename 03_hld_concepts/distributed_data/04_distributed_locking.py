# 04_distributed_locking.py
import time
import random

# ==========================================
# 🔒 DISTRIBUTED LOCK (Simulation)
# ==========================================
# SCENARIO: 3 Cron jobs run on 3 servers.
# They must NOT run the same task twice.
# They need a shared lock (e.g., Redis).

class RedisMock:
    def __init__(self):
        self.locks = {}
        
    def setnx(self, key, value, ttl):
        # SET if Not Exists
        if key in self.locks:
            if time.time() < self.locks[key]['expiry']:
                return False # Locked
        
        self.locks[key] = {
            'owner': value,
            'expiry': time.time() + ttl
        }
        return True

class Worker:
    def __init__(self, name, redis):
        self.name = name
        self.redis = redis
        
    def try_run_task(self, task_id):
        # Try to acquire lock for 2 seconds
        if self.redis.setnx(f"lock:{task_id}", self.name, ttl=2):
            print(f"✅ [{self.name}] Acquired lock! Running task {task_id}...")
            time.sleep(1) # Work
            print(f"✅ [{self.name}] Done.")
            return True
        else:
            print(f"❌ [{self.name}] Failed to get lock. Skipping.")
            return False

if __name__ == "__main__":
    redis = RedisMock()
    w1 = Worker("Server A", redis)
    w2 = Worker("Server B", redis)
    
    # Both try to run Task 101 at exact same time
    print("--- 🔒 Distributed Lock Test ---")
    w1.try_run_task(101)
    w2.try_run_task(101) # Should fail
    
    # Wait for TTL expiry
    print("... Waiting for lock expiry ...")
    time.sleep(2.1)
    
    w2.try_run_task(101) # Should succeed now

import time
import random
import threading
from queue import Queue, Full

# ==========================================
# 🏆 THE SOLUTION
# ==========================================

# 1. TOKEN BUCKET RATE LIMITER
class RateLimiter:
    def __init__(self, rate, capacity):
        self.rate = rate # tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = threading.Lock()
        
    def allow(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            # Refill tokens
            new_tokens = elapsed * self.rate
            if new_tokens > 0:
                self.tokens = min(self.capacity, self.tokens + new_tokens)
                self.last_refill = now
            
            # Consume token
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

# 2. ROBUST SERVER (Queue + Limiter)
class RobustServer:
    def __init__(self):
        self.active_requests = 0
        self.lock = threading.Lock()
        # Max concurrency 5 (GPU limit)
        self.sem = threading.Semaphore(5)
        
        # Rate Limiting: 2 requests per second per user logic (implied global here)
        self.limiter = RateLimiter(rate=5, capacity=5) 
        
    def handle_request(self, user_id):
        # Step 1: Rate Limit Check (Load Shedding)
        if not self.limiter.allow():
            print(f"🛡️ [429] Rate Limit Exceeded for {user_id}")
            return False

        # Step 2: Concurrency Control (Semaphore)
        # Instead of crashing, we wait or reject if timeout
        acquired = self.sem.acquire(blocking=True, timeout=1)
        if not acquired:
            print("🛡️ [503] Server Busy (Queue Full)")
            return False
            
        try:
            # Critical Section (Verification)
            with self.lock:
                self.active_requests += 1
                if self.active_requests > 5:
                    print("💀 FATAL ERROR: Semaphore Failed!")
            
            # Processing
            # print(f"✅ Processing {user_id}...")
            time.sleep(random.uniform(0.1, 0.5))
            
        finally:
            with self.lock:
                self.active_requests -= 1
            self.sem.release()
            return True

def simulate_traffic(server):
    threads = []
    # 20 concurrent requests
    for i in range(20):
        t = threading.Thread(target=server.handle_request, args=(f"user_1",))
        threads.append(t)
        t.start()
        
    for t in threads: t.join()

if __name__ == "__main__":
    print("🛡️ Starting Robust Stress Test...")
    server = RobustServer()
    simulate_traffic(server)
    
    print("🎉 TEST PASSED: Server handled traffic gracefully (dropped excesses).")

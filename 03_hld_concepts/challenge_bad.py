import time
import random
import threading

# ==========================================
# 💀 THE CHALLENGE: SURVIVE THE TRAFFIC SPIKE
# ==========================================
# SCENARIO:
# You operate a popular LLM API.
# SUDDENLY: 100 users hit you at once.
# Your GPU can only handle 5 requests per second (Concurrent).
#
# PROBLEMS:
# 1. No Rate Limiting. One user spamming loop crashes the server.
# 2. No Queue management. Requests pile up until memory explodes.
# 3. Simulation of "Server Crash" if active_requests > 5.
#
# GOAL:
# Refactor using:
# - A Token Bucket or Leaky Bucket Rate Limiter.
# - A Request Queue (Producer/Consumer).
# - Drop requests immediately if queue is full (Load Shedding).

class VulnerableServer:
    def __init__(self):
        self.active_requests = 0
        self.lock = threading.Lock()
        self.crashed = False
        
    def handle_request(self, user_id):
        if self.crashed: return False
        
        with self.lock:
            self.active_requests += 1
            if self.active_requests > 5:
                print(f"💀 CRASH! Too many requests ({self.active_requests})")
                self.crashed = True
                return False
                
        # Simulate Processing
        time.sleep(random.uniform(0.1, 0.5))
        
        with self.lock:
            self.active_requests -= 1
        return True

def simulate_traffic(server):
    # One malicious user sends 20 requests instantly
    threads = []
    for i in range(20):
        t = threading.Thread(target=server.handle_request, args=(f"user_1",))
        threads.append(t)
        t.start()
        
    for t in threads: t.join()

if __name__ == "__main__":
    print("💀 Starting Stress Test...")
    server = VulnerableServer()
    simulate_traffic(server)
    
    if server.crashed:
        print("💀 TEST FAILED: Server Crashed.")
    else:
        print("🎉 TEST PASSED: Server Survived.")

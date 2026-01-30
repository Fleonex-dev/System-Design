import time
import random
from queue import Queue

# ==========================================
# 🛑 THE SCREW UP (Round Robin on Heterogeneous Load)
# ==========================================
# SCENARIO: 
# Request 1: "Write a novel" (Takes 5s) -> Goes to Server A
# Request 2: "Hi" (Takes 0.1s) -> Goes to Server B
# Request 3: "Hi" (Takes 0.1s) -> Goes to Server A (BLOCKED by Request 1)
# Request 4: "Hi" (Takes 0.1s) -> Goes to Server B
#
# Result: Request 3 is blocked for 5s, even though Server B was free!

class Server:
    def __init__(self, name):
        self.name = name
        self.busy_until = 0 # Unix Timestamp
        
    def is_busy(self):
        return time.time() < self.busy_until

    def process(self, duration):
        # Simulate processing time
        self.busy_until = time.time() + duration

def run_the_screwup():
    print("🛑 [Bad] Round Robin Balancing...")
    servers = [Server("A"), Server("B")]
    requests = [5.0, 0.1, 0.1, 0.1] # Duration of tasks
    
    for i, duration in enumerate(requests):
        # Round Robin Logic: (i % len)
        target = servers[i % len(servers)]
        
        wait_time = max(0, target.busy_until - time.time())
        print(f"🛑 Req {i} ({duration}s) -> {target.name} (Wait: {wait_time:.1f}s)")
        
        target.process(duration)
        
    print("🛑 Notice Req 2 waited for Server A, even though B was free!")

# ==========================================
# ✅ THE FIX (Least Connections / Lease Recently Used)
# ==========================================
# SCENARIO: Check who is free. Route to them.

def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (Least Connections) ---")
    servers = [Server("A"), Server("B")]
    requests = [5.0, 0.1, 0.1, 0.1]
    
    for i, duration in enumerate(requests):
        # Find server with minimum 'busy_until'
        target = min(servers, key=lambda s: s.busy_until)
        
        wait_time = max(0, target.busy_until - time.time())
        print(f"✅ Req {i} ({duration}s) -> {target.name} (Wait: {wait_time:.1f}s)")
        
        target.process(duration)

if __name__ == "__main__":
    print("🧪 LOAD BALANCING TEST: Round Robin (Bad) vs Least Conn (Good)\n")
    run_the_screwup()
    run_the_fix()
    
    print("\n🏆 Conclusion: For LLMs (variable compute time), Round Robin is FATAL. Use Least-Connections.")

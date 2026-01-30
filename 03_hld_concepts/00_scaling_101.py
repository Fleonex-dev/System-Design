# 00_scaling_101.py
import time
import random

# ==========================================
# 📈 SCALING 101: VERTICAL VS HORIZONTAL
# ==========================================

class Server:
    def __init__(self, name, power=1):
        self.name = name
        self.power = power # Requests per second capacity
        self.busy = False
        
    def handle_request(self):
        if self.busy:
            return False # Dropped
        self.busy = True
        # Simulate processing time based on power (More power = Faster)
        time.sleep(1.0 / self.power)
        self.busy = False
        return True

def run_simulation(strategy, servers, requests):
    print(f"\n--- Strategy: {strategy} ---")
    dropped = 0
    start = time.time()
    
    for _ in range(requests):
        # Round robin load balancing
        captured = False
        for s in servers:
            if s.handle_request():
                print(f"   ✅ Handled by {s.name}")
                captured = True
                break
        
        if not captured:
            print("   ❌ Dropped (All Busy)")
            dropped += 1
            
    total_time = time.time() - start
    print(f"📊 Result: {requests - dropped}/{requests} success. Time: {total_time:.2f}s")

if __name__ == "__main__":
    # Baseline: 1 Small Server
    # 1. Vertical Scaling: Buy a SUPER COMPUTER (Power=5)
    # 2. Horizontal Scaling: Buy 5 CHEAP COMPUTERS (Power=1)
    
    reqs = 5
    
    print("1️⃣  Vertical Scaling (Upgrade RAM/CPU)")
    big_box = [Server("SuperServer", power=5)]
    run_simulation("Vertical", big_box, reqs)
    
    print("\n2️⃣  Horizontal Scaling (Add Nodes)")
    cluster = [Server(f"Node-{i}", power=1) for i in range(5)]
    run_simulation("Horizontal", cluster, reqs)
    
    print("\n🏆 Insight: Horizontal is usually better for 'Stateless' apps because you can scale infinitely.")
    print("   Vertical hits a hardware limit (Max 128 Cores).")

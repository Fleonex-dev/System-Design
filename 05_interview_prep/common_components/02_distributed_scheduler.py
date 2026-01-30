# 02_distributed_scheduler.py
import time
import random

# ==========================================
# ⏱️ DISTRIBUTED SCHEDULER
# ==========================================
# SCENARIO: You have 3 servers. You need to run "Daily Report" at 12:00.
# If all 3 run it, you charge the user 3 times. BAD.
# Soluton: Leader Election. Only LEADER schedules tasks.

class ServerNode:
    def __init__(self, id):
        self.id = id
        self.is_leader = False
        self.last_heartbeat = 0
        
    def try_become_leader(self, shared_storage):
        # Atomic "SET IF NOT EXISTS"
        current_leader = shared_storage.get("leader")
        now = time.time()
        
        if current_leader is None or (now - shared_storage.get("hb", 0) > 2):
            # Leader dead or empty. I take over.
            shared_storage["leader"] = self.id
            shared_storage["hb"] = now
            self.is_leader = True
            print(f"👑 [{self.id}] I am the Leader now!")
        elif current_leader == self.id:
            # I am still leader, renew lease
            shared_storage["hb"] = now
            self.is_leader = True
        else:
            self.is_leader = False
            print(f"💤 [{self.id}] Following leader {current_leader}...")

    def run_cron(self):
        if self.is_leader:
            print(f"   🚀 [{self.id}] Executing CRON JOB...")

if __name__ == "__main__":
    store = {} # Mock Redis
    nodes = [ServerNode("A"), ServerNode("B"), ServerNode("C")]
    
    print("--- ⏱️ Tick 1 (Election) ---")
    for n in nodes: n.try_become_leader(store)
    for n in nodes: n.run_cron()
    
    print("\n--- ⏱️ Tick 2 (Stability) ---")
    for n in nodes: n.try_become_leader(store)
    
    print("\n--- 💀 Leader A Dies ---")
    store["hb"] = time.time() - 5 # Simulate timeout
    
    print("--- ⏱️ Tick 3 (Re-Election) ---")
    nodes[1].try_become_leader(store) # Node B checks
    nodes[1].run_cron()

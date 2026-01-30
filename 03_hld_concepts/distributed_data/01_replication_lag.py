# 01_replication_lag.py
import time
import random

# ==========================================
# 🛑 THE SCREW UP (Read-After-Write Consistency)
# ==========================================
# SCENARIO: User posts a comment -> Saved to Master DB.
# Master replicates to Slave DB (takes 100ms).
# User immediately refreshes page -> Reads from Slave DB.
# Comment is missing! User thinks "It vanished?!".

class DatabaseCluster:
    def __init__(self):
        self.master_data = {}
        self.slave_data = {}
        self.lag_ms = 0.5 # 500ms lag
        
    def write_master(self, key, value):
        print(f"📝 [Master] Wrote {key}={value}")
        self.master_data[key] = { "val": value, "ts": time.time() }
        
    def read_slave(self, key):
        # Simulate replication delay
        if key in self.master_data:
            written_at = self.master_data[key]["ts"]
            if time.time() - written_at < self.lag_ms:
                return None # Not replicated yet!
            return self.master_data[key]["val"]
        return None

def run_simulation():
    db = DatabaseCluster()
    
    print("--- 🛑 Scenario: Replication Lag ---")
    # 1. User writes
    db.write_master("comment:1", "Hello World")
    
    # 2. User reads immediately (10ms later)
    time.sleep(0.01)
    result = db.read_slave("comment:1")
    
    if result is None:
        print("❌ [Slave] Read failed! Data not found (Lag).")
    else:
        print(f"✅ [Slave] Read: {result}")
        
    # 3. User waits and reads again
    print("... User waits 1s ...")
    time.sleep(0.6)
    result = db.read_slave("comment:1")
    print(f"✅ [Slave] Read: {result} (Eventually Consistent)")

if __name__ == "__main__":
    run_simulation()
    print("\n🏆 Fixes: Sticky Session (Read own writes from Master) or Version Monotonicity.")

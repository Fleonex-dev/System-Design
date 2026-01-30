# 03_cap_theorem.py
import time

# ==========================================
# 🧠 CAP THEOREM SIMULATION
# ==========================================
# Theorem: In a distributed system with a Partition (network cut),
# You must choose between Consistency (C) and Availability (A).
# You CANNOT have both.

class Node:
    def __init__(self, name, mode):
        self.name = name
        self.data = "v1"
        self.is_connected = True
        self.mode = mode # 'CP' or 'AP'
        
    def receive_update(self, new_data):
        if not self.is_connected:
            print(f"   ⚠️  [{self.name}] Network Partition! Cannot sync.")
            return False
        self.data = new_data
        return True
        
    def read(self):
        if self.mode == 'CP' and not self.is_connected:
            return "ERROR: 503 Service Unavailable (Maintaining Consistency)"
        
        # AP Mode returns data even if disconnected (potentially stale)
        return self.data

def run_simulation():
    print("--- 🧠 CP System (Bank) ---")
    # Partition happens!
    node = Node("BankNode", mode='CP')
    node.is_connected = False # Cut wire
    
    print("User writes 'v2' to Master...")
    # Master fails to replicate to this node
    node.receive_update("v2") 
    
    print(f"User reads from Node: '{node.read()}'")
    print("✅ System chose Consistency over Availability.\n")
    
    print("--- 🧠 AP System (Social Media) ---")
    node = Node("SocialNode", mode='AP')
    node.is_connected = False
    
    print("User writes 'v2' to Master...")
    node.receive_update("v2") # Fails to sync
    
    print(f"User reads from Node: '{node.read()}'")
    print("✅ System chose Availability (served stale 'v1') over Consistency.")

if __name__ == "__main__":
    run_simulation()

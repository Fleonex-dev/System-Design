import hashlib

# ==========================================
# 🛑 THE SCREW UP (Modulo Hashing)
# ==========================================
# SCENARIO: You serve users from 3 DB nodes.
# key_id % 3 determines the node.
# You add a 4th node.
# key_id % 4 changes the location for ALMOST EVERY KEY.
# Result: 100% Cache Miss storm. Database crashes.

def get_node_bad(key, num_nodes):
    # Standard modulo routing
    h = int(hashlib.md5(key.encode()).hexdigest(), 16)
    return h % num_nodes

def run_the_screwup():
    print("🛑 [Bad] Modulo Hashing...")
    keys = [f"user_{i}" for i in range(10)]
    
    # Map to 3 nodes
    mapping_3 = {k: get_node_bad(k, 3) for k in keys}
    
    # Scale up! Add 1 node.
    mapping_4 = {k: get_node_bad(k, 4) for k in keys}
    
    moved_count = 0
    for k in keys:
        if mapping_3[k] != mapping_4[k]:
            moved_count += 1
            
    print(f"🛑 Resharding from 3->4 nodes moved {moved_count}/{len(keys)} keys.")
    print("🛑 Ideally, only 1/4 (25%) should move. Here it's drastic.")


# ==========================================
# ✅ THE FIX (Consistent Hashing)
# ==========================================
# SCENARIO: Place nodes on a ring (0-360 degrees).
# Place keys on the same ring.
# Move clockwise to find the nearest node.
# Adding a node only takes keys from its "clockwise neighbor".

class ConsistentHashRing:
    def __init__(self, nodes, replicas=3):
        self.replicas = replicas
        self.ring = {}
        self.sorted_keys = []
        
        for node in nodes:
            self.add_node(node)
            
    def add_node(self, node):
        for i in range(self.replicas):
            key = self._hash(f"{node}_{i}")
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()
        
    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
        
    def get_node(self, key):
        h = self._hash(key)
        # Binary search could be used here for speed
        for k in self.sorted_keys:
            if h <= k:
                return self.ring[k]
        # Wrap around
        return self.ring[self.sorted_keys[0]]

def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (Consistent Ring) ---")
    keys = [f"user_{i}" for i in range(100)]
    
    # 3 Nodes
    ch = ConsistentHashRing(["NodeA", "NodeB", "NodeC"])
    start_map = {k: ch.get_node(k) for k in keys}
    
    # Add Node D
    print("✅ Adding NodeD...")
    ch.add_node("NodeD")
    end_map = {k: ch.get_node(k) for k in keys}
    
    moved_count = 0
    for k in keys:
        if start_map[k] != end_map[k]:
            moved_count += 1
            
    # Theoretical ideal is 1/4 = 25 keys moving
    print(f"✅ Moved {moved_count}/{len(keys)} keys.")
    print("✅ This minimizes cache miss storms.")

if __name__ == "__main__":
    print("🧪 HASHING TEST: Modulo (Bad) vs Consistent Ring (Good)\n")
    run_the_screwup()
    run_the_fix()
    
    print("\n🏆 Insight: Consistent Hashing minimizes data movement when nodes are added/removed.")
    print("   🏢 Real World: **Discord** uses this for their Chat Ring Servers.")
    print("   **Amazon DynamoDB** uses this to partition data across storage nodes.")
    print("   **Cassandra** uses 'Virtual Nodes' (vnodes) on top of this ring.")

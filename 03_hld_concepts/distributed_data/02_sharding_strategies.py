# 02_sharding_strategies.py
import hashlib

# ==========================================
# 🍰 SHARDING STRATEGIES
# ==========================================
# SCENARIO: 1TB of Data. Split across 4 nodes.

nodes = ["Node-A", "Node-B", "Node-C", "Node-D"]

# 1. RANGE BASED (e.g., Google BigTable, HBase)
# Key: User Name.
# A-F -> Node 1
# G-L -> Node 2...
# PRO: Range scans are fast ("Give me all users A*")
# CON: Hotspots! (If everyone is named "Alice", Node 1 dies).
def range_sharding(key):
    first_char = key[0].upper()
    if first_char < 'G': return nodes[0]
    if first_char < 'M': return nodes[1]
    if first_char < 'S': return nodes[2]
    return nodes[3]

# 2. HASH BASED (e.g., DynamoDB, Cassandra)
# Key: User Name.
# Hash(Key) % 4 -> Node.
# PRO: Uniform distribution (No hotspots usually).
# CON: Range scans are impossible (Alice is on Node 1, Bob on Node 3).
def hash_sharding(key):
    # MD5 hash -> Integer
    h = int(hashlib.md5(key.encode()).hexdigest(), 16)
    idx = h % len(nodes)
    return nodes[idx]

if __name__ == "__main__":
    users = ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank", "George", "Zack"]
    
    print("--- 📏 Range Sharding ---")
    # Notice how Node-A gets HAMMERED
    for u in users:
        print(f"User {u:7} -> {range_sharding(u)}")
        
    print("\n--- 🎲 Hash Sharding ---")
    # Notice better spread (random-ish)
    for u in users:
        print(f"User {u:7} -> {hash_sharding(u)}")
        
    print("\n🏆 Rule: Use Range if you need 'Select * where date > X'. Use Hash for simple KV lookups.")

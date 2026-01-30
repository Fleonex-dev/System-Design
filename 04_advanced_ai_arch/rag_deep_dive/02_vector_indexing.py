# 02_vector_indexing.py
import random
import math

# ==========================================
# 🔍 VECTOR INDEXING (The "Magic" of Search)
# ==========================================
# SCENARIO: You have 1 Million vectors.
# Brute Force scan = O(N). Too slow (1s).
# HNSW (Graph) = O(log N). Fast (5ms).

class VectorDBNode:
    def __init__(self, id, vector):
        self.id = id
        self.vector = vector
        self.neighbors = [] # The "connections" in the graph

def euclidean_dist(v1, v2):
    return math.sqrt(sum((a-b)**2 for a, b in zip(v1, v2)))

def build_small_world_graph(nodes):
    print("--- 🏗️ Building HNSW Graph (Simulated) ---")
    # Connect everything to random 2 neighbors (Simulating layers)
    for node in nodes:
        targets = random.sample(nodes, 2)
        node.neighbors = targets
        print(f"   Node {node.id} <-> {[n.id for n in targets]}")

def search_graph(entry_node, query_vector):
    print(f"\n--- 🔍 GREEDY SEARCH (Start at Node {entry_node.id}) ---")
    current = entry_node
    best_dist = euclidean_dist(current.vector, query_vector)
    
    steps = 0
    while True:
        steps += 1
        found_better = False
        
        # Look at neighbors
        for neighbor in current.neighbors:
            dist = euclidean_dist(neighbor.vector, query_vector)
            if dist < best_dist:
                print(f"   Step {steps}: Moving to Node {neighbor.id} (Dist: {dist:.2f})")
                best_dist = dist
                current = neighbor
                found_better = True
        
        if not found_better:
            print(f"   ✅ Local Minima Found at Node {current.id}")
            break
            
    return current

if __name__ == "__main__":
    # Create random vectors
    nodes = [VectorDBNode(i, [random.random(), random.random()]) for i in range(10)]
    build_small_world_graph(nodes)
    
    # Search
    search_graph(nodes[0], [0.5, 0.5])

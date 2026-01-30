# optimal.py
import hashlib

# ==========================================
# ✅ OPTIMAL: COUNT-MIN SKETCH (Probabilistic)
# ==========================================
# STRATEGY:
# 1. Fixed size matrix (e.g., 5 rows x 1000 cols).
# 2. Hash word 5 times -> Increment 5 cells.
# 3. Frequency is approx min(cells).
#
# RESULT: Count billions of items with fixed KB/MB memory. Error rate is mathematically bounded.

class CountMinSketch:
    def __init__(self, width=100, depth=5):
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]
        
    def add(self, item):
        for i in range(self.depth):
            # Simulate different hash functions using salt
            h = int(hashlib.md5((item + str(i)).encode()).hexdigest(), 16) % self.width
            self.table[i][h] += 1
            
    def estimate(self, item):
        min_count = float('inf')
        for i in range(self.depth):
            h = int(hashlib.md5((item + str(i)).encode()).hexdigest(), 16) % self.width
            min_count = min(min_count, self.table[i][h])
        return min_count

if __name__ == "__main__":
    print("--- 📉 Count-Min Sketch Demo ---")
    cms = CountMinSketch()
    
    data = ["cat"]*100 + ["dog"]*50 + ["mouse"]*5
    for w in data: cms.add(w)
    
    print(f"Est 'cat': {cms.estimate('cat')} (Real: 100)")
    print(f"Est 'dog': {cms.estimate('dog')} (Real: 50)")
    
    print("\n🏆 Insight: We counted frequencies using a tiny fixed array.")
    print("   Used by **Twitter** (Trending) and **Amazon** (Top Sellers).")
    print("   Tradeoff: Small chance of over-counting (Collision), but never under-counting.")

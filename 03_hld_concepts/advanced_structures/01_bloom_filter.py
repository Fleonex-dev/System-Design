# 01_bloom_filter.py
import hashlib

# ==========================================
# 🌸 BLOOM FILTER
# ==========================================
# SCENARIO: Have we seen this user before?
# Set of 1 Billion Users.
# BAD: Store 1B strings (Terabytes).
# GOOD: Bloom Filter (Kilobytes).
# Tradeoff: "No" is 100% Certain. "Yes" is Maybe (False Positive).

class SimpleBloomFilter:
    def __init__(self, size=100):
        self.size = size
        self.bit_array = [0] * size
        
    def _hashes(self, item):
        # We simulate 2 hash functions using diff algos
        h1 = int(hashlib.md5(item.encode()).hexdigest(), 16) % self.size
        h2 = int(hashlib.sha1(item.encode()).hexdigest(), 16) % self.size
        return h1, h2
        
    def add(self, item):
        h1, h2 = self._hashes(item)
        self.bit_array[h1] = 1
        self.bit_array[h2] = 1
        print(f"➕ Added '{item}': Bits {h1}, {h2} set.")
        
    def check(self, item):
        h1, h2 = self._hashes(item)
        if self.bit_array[h1] == 1 and self.bit_array[h2] == 1:
            return "Probably YES" # False Positive possible
        return "Definitely NO"

if __name__ == "__main__":
    print("--- 🌸 Bloom Filter Demo ---")
    bf = SimpleBloomFilter(size=20) # Very small to force collisions
    
    bf.add("apple")
    bf.add("banana")
    
    print(f"\nChecking 'apple': {bf.check('apple')}")
    print(f"Checking 'carrot': {bf.check('carrot')}")
    
    print("\n--- 💥 Simulating False Positive ---")
    # In a tiny array of size 20, collisions are likely
    # Real BF uses size ~ Millions
    print(f"Bit Array: {bf.bit_array}")
    
    print("\n🏆 Insight: Very fast, very small memory footprint.")
    print("   🏢 Real World: **Google Chrome** uses it to check malicious URLs locally.")
    print("   **Cassandra/DynamoDB** use it to skip checking disk SSTables if a key doesn't exist.")

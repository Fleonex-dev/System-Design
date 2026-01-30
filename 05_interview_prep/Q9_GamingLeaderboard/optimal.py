# optimal.py
import heapq

# ==========================================
# ✅ OPTIMAL: REDIS SORTED SET (ZSET)
# ==========================================
# STRATEGY:
# 1. Store scores in a data structure that STAYS sorted (SkipList).
# 2. Redis `ZADD` is O(log N).
# 3. Redis `ZRANGE` is O(log N + K). Fast.

class MockRedisZSet:
    def __init__(self):
        self.data = {}
        
    def zadd(self, player, score):
        # In reality, Redis uses a SkipList to keep this sorted efficiently
        self.data[player] = score
        
    def zrevrange(self, k):
        # Get Top K
        print("   🚀 Fetching Top K from Sorted Set (No Scan needed)...")
        sorted_items = sorted(self.data.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:k]

if __name__ == "__main__":
    print("--- 🎮 Real-Time Leaderboard ---")
    redis = MockRedisZSet()
    
    # Real-time updates
    redis.zadd("Alice", 100)
    redis.zadd("Bob", 50)
    redis.zadd("Charlie", 150)
    
    # Instant Retrieval
    top = redis.zrevrange(3)
    print(f"Leaderboard: {top}")
    
    print("\n🏆 Insight: Use **Redis Sorted Sets (ZSET)**.")
    print("   SQL cannot handle 'Rank Calculation' for millions of users in real-time.")

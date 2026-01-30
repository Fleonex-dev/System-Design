# 04_lru_cache.py

# ==========================================
# 🧠 LRU CACHE (Least Recently Used)
# ==========================================
# SCENARIO: Cache size is 3.
# Add A, B, C. Cache: [A, B, C]
# Access A. Cache: [B, C, A] (A is newest)
# Add D. Cache: [C, A, D] (B was evicted because it was oldest)
#
# REQUIREMENT: Get() and Put() must be O(1).
# SOLUTION: HashMap (for lookup) + Doubly Linked List (for ordering).

class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {} # Map Key -> Node
        # Dummy head/tail for easy removal/addition
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        
    def _remove(self, node):
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = prev
        
    def _add_to_end(self, node):
        # Add before tail (Make it newest)
        prev = self.tail.prev
        prev.next = node
        node.prev = prev
        node.next = self.tail
        self.tail.prev = node
        
    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            # Move to end (Recently Used)
            self._remove(node)
            self._add_to_end(node)
            return node.val
        return -1
        
    def put(self, key, value):
        if key in self.cache:
            # Update existing
            self._remove(self.cache[key])
        
        new_node = Node(key, value)
        self._add_to_end(new_node)
        self.cache[key] = new_node
        
        if len(self.cache) > self.capacity:
            # Evict LRU (First item after head)
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]
            print(f"   🗑️ Evicted key: {lru.key}")

if __name__ == "__main__":
    print("--- 🧠 LRU Cache Demo (O(1)) ---")
    lru = LRUCache(2) # Capacity 2
    
    print("Put A, Put B...")
    lru.put("A", 1)
    lru.put("B", 2)
    print(f"Get A: {lru.get('A')} (A is now newest)")
    
    print("Put C (Should evict B)...")
    lru.put("C", 3)
    
    print(f"Get B: {lru.get('B')} (Should be -1)")
    print(f"Get C: {lru.get('C')}")
    
    print("\n🏆 Insight: O(1) implies Hash Map. Ordering implies Linked List. Using BOTH is the trick.")

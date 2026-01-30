# 05_trie_autocomplete.py

# ==========================================
# 🌳 TRIE (Prefix Tree)
# ==========================================
# SCENARIO: Typeahead. User types "ca".
# We need to find "cat", "car", "cart", "cake".
# Scanning a list of 1B words is O(N). Too slow.
# Trie search is O(L) where L is length of prefix (e.g., 2). BLAZING FAST.

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.freq = 0 # For ranking suggestions

class Trie:
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.freq += 1 # This prefix is more popular now
        node.is_end_of_word = True
        
    def search_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # DFS to find all words from this node
        results = []
        self._dfs(node, prefix, results)
        return results
        
    def _dfs(self, node, prefix, results):
        if len(results) >= 5: return # Top 5 only
        if node.is_end_of_word:
            results.append(prefix)
            
        # Sort children by frequency (optional optimization)
        for char, child in node.children.items():
            self._dfs(child, prefix + char, results)

if __name__ == "__main__":
    print("--- 🌳 Trie Typeahead Demo ---")
    trie = Trie()
    words = ["car", "cat", "cart", "cake", "carbon", "hello", "help"]
    for w in words: trie.insert(w)
    
    query = "ca"
    print(f"User types: '{query}'")
    suggestions = trie.search_prefix(query)
    print(f"Suggestions: {suggestions}")
    
    print("\n🏆 Insight: Tries compress shared prefixes. 'Car' and 'Cat' share 'Ca'.")
    print("   🏢 Real World: **Google Search**, **Algolia**, **ElasticSearch** (FSTs).")

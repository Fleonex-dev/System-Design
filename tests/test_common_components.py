
import pytest
import sys
import os

# Add root to path so we can import modules
sys.path.append(os.getcwd())

# We need to import the classes.
# Since the file structure is nested, we can import by file path or use sys.path hacks.
# Best practice for this repo structure is simpler: Import directly if possible.

# Import specific implementation files
# We use importlib because filenames like '04_lru_cache.py' are not valid standard identifiers without renaming.
import importlib.util

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# Load implementations
lru_mod = load_module("lru_cache", "05_interview_prep/common_components/04_lru_cache.py")
trie_mod = load_module("trie", "05_interview_prep/common_components/05_trie_autocomplete.py")
token_mod = load_module("token_bucket", "05_interview_prep/common_components/06_token_bucket.py")

class TestLRUCache:
    def test_lru_eviction(self):
        cache = lru_mod.LRUCache(capacity=2)
        cache.put("A", 1)
        cache.put("B", 2)
        assert cache.get("A") == 1
        
        # Add C, should evict B (since A was just accessed)
        cache.put("C", 3)
        assert cache.get("B") == -1 # Evicted
        assert cache.get("C") == 3
        assert cache.get("A") == 1
        
    def test_update_existing(self):
        cache = lru_mod.LRUCache(2)
        cache.put("A", 1)
        cache.put("A", 10) # Update
        assert cache.get("A") == 10
        assert len(cache.cache) == 1

class TestTrie:
    def test_insert_search(self):
        trie = trie_mod.Trie()
        trie.insert("apple")
        trie.insert("app")
        
        res = trie.search_prefix("ap")
        assert "apple" in res
        assert "app" in res
        
        res2 = trie.search_prefix("zoo")
        assert res2 == []

class TestTokenBucket:
    def test_bursts(self):
        bucket = token_mod.TokenBucket(capacity=5, refill_rate=100) # Fast refill
        # Should allow 5 immediately
        assert bucket.consume(5) == True
        # Should fail 6th (if we assume instantaneous consumption greater than refill in this microsecond thread window, but refill is fast)
        
        # Let's test standard rate
        bucket = token_mod.TokenBucket(capacity=1, refill_rate=0.1)
        assert bucket.consume(1) == True
        assert bucket.consume(1) == False # Empty

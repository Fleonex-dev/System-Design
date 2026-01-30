# bad.py
from collections import Counter

# ==========================================
# 🛑 BAD: EXACT COUNTING (HashMap)
# ==========================================
# SCENARIO: Twitter Trending Topics. 500M Tweets/day.
# NAIVE: HashMap<String, Int> for every word.
# PROBLEM:
# 1. Memory! Storing every unique word/hashtag uses Perabytes of RAM.
# 2. Garbage Collection hell.

class ExactCounter:
    def __init__(self):
        self.counts = Counter()
        
    def ingest(self, text):
        words = text.split()
        for w in words:
            self.counts[w] += 1
            
    def get_top(self):
        # Sorting millions of keys is slow
        return self.counts.most_common(3)

if __name__ == "__main__":
    c = ExactCounter()
    c.ingest("cat dog cat mouse dog dog")
    print(c.get_top())

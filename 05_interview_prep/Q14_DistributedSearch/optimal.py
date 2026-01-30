# optimal.py

# ==========================================
# ✅ OPTIMAL: INVERTED INDEX (Elasticsearch)
# ==========================================
# STRATEGY:
# 1. Pre-process (Index): Split documents into tokens.
# 2. Map Token -> List[DocID].
# 3. Query is O(1) hash lookup.

class InvertedIndex:
    def __init__(self):
        self.index = {} # Token -> [DocIDs]
        self.docs = {}
        
    def index_doc(self, id, text):
        self.docs[id] = text
        for token in text.lower().split():
            if token not in self.index: self.index[token] = []
            self.index[token].append(id)
            
    def search(self, query):
        print(f"   🔎 Lookup '{query}' in Index...")
        doc_ids = self.index.get(query.lower(), [])
        return [self.docs[i] for i in doc_ids]

if __name__ == "__main__":
    es = InvertedIndex()
    es.index_doc(1, "INFO start server")
    es.index_doc(2, "ERROR database crash")
    es.index_doc(3, "INFO end process")
    
    # Instant lookup
    results = es.search("ERROR")
    print(f"Results: {results}")
    
    print("\n🏆 Insight: Inverted Indexes power **Google** and **Elasticsearch**.")
    print("   In distributed systems, we shard this index by DocID (Scatter-Gather).")

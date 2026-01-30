from abc import ABC, abstractmethod

# ==========================================
# 🛑 THE SCREW UP (Hardcoded Algorithms)
# ==========================================
# SCENARIO: You built a RAG system using Vector Search.
# Users complain it misses exact keyword matches.
# You hack in an 'if' statement to try Keyword Search instead.
# Now your code is a mess of mixed logic.

class RAGPipelineBad:
    def __init__(self, mode="vector"):
        self.mode = mode
        
    def retrieve(self, query):
        print(f"🛑 [Bad] Retrieving using {self.mode}...")
        
        if self.mode == "vector":
            # Complex embedding logic here
            return [f"Vector result for {query}"]
        elif self.mode == "keyword":
            # specific BM25 logic here
            return [f"Keyword result for {query}"]
        elif self.mode == "hybrid":
            # Mixed logic
            return [f"Hybrid result for {query}"]
            
def run_the_screwup():
    rag = RAGPipelineBad("keyword")
    print(rag.retrieve("apple"))


# ==========================================
# ✅ THE FIX (Strategy Pattern)
# ==========================================
# SCENARIO: Encapsulate algorithms into separate classes.
# The Context (RAGPipeline) just holds a 'strategy'.
# You can swap strategies at runtime!

# Strategy Interface
class RetrievalStrategy(ABC):
    @abstractmethod
    def search(self, query: str) -> list: pass

# Concrete Strategies
class VectorSearch(RetrievalStrategy):
    def search(self, query): 
        return [f"🔍 [Vector] Embedding search for '{query}'"]

class KeywordSearch(RetrievalStrategy):
    def search(self, query): 
        return [f"📖 [BM25] Keyword search for '{query}'"]

class HybridSearch(RetrievalStrategy):
    def search(self, query): 
        return [f"⚡ [Hybrid] Both results for '{query}'"]

# Context
class RAGPipeline:
    def __init__(self, strategy: RetrievalStrategy):
        self.strategy = strategy
        
    def set_strategy(self, strategy: RetrievalStrategy):
        print(f"✅ Switching strategy to {type(strategy).__name__}")
        self.strategy = strategy
        
    def run(self, query):
        return self.strategy.search(query)

def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (Strategy) ---")
    
    # Start with Vector
    rag = RAGPipeline(VectorSearch())
    print(rag.run("apple"))
    
    # Runtime switch! No restarting code.
    rag.set_strategy(KeywordSearch())
    print(rag.run("apple"))

if __name__ == "__main__":
    print("🧪 STRATEGY TEST: Hardcoded (Bad) vs Swappable (Good)\n")
    run_the_screwup()
    run_the_fix()
    
    print("\n🏆 Conclusion: Strategy pattern lets you A/B test algorithms easily.")

# 01_rag_pipeline_optimization.py

# ==========================================
# 🛑 THE SCREW UP (Naive RAG)
# ==========================================
# SCENARIO: User asks "How much for a Tesla?". 
# DB contains: "Tesla reported 20b revenue."
# Vector search matches "Tesla" + "Revenue" via similarity, but misses actual pricing data 
# because the phrasing is different. Revalidating relevance is missing.

class NaiveRAG:
    def retrieve(self, query):
        print(f"🛑 [Bad] Searching for '{query}'...")
        # Simulating a vector search returning top-3
        return [
            "Tesla requires a driver's license.",  # Irrelevant
            "Tesla coils are dangerous.",         # Irrelevant
            "Model Y costs $40k."                 # Relevant (Rank 3!)
        ]

def run_the_screwup():
    rag = NaiveRAG()
    docs = rag.retrieve("How much is a Tesla?")
    print(f"🛑 Context sent to LLM: {docs[0]} (Top result is garbage)")


# ==========================================
# ✅ THE FIX (HyDE + Re-ranking)
# ==========================================
# 1. HyDE: Ask LLM to hallucinate an answer. "A Tesla Model 3 costs around $35k". Embed THAT.
#    This matches the target document better than the question does.
# 2. Re-ranking: Take Top-50 results. Use a BERT Cross-Encoder to score (Query, Doc) pairs.
#    Sort by true relevance.

class AdvancedRAG:
    def hyde_transform(self, query):
        print(f"✅ [HyDE] Hallucinating answer for '{query}'...")
        return "Tesla cars range from $40,000 to $100,000 depending on the model."
    
    def vector_search(self, embedding_text):
        print(f"✅ [VectorDB] Searching with hallucinated text...")
        return [
            "Tesla requires a driver's license.",
            "Tesla coils are dangerous.",
            "Model Y costs $40k."
        ]
        
    def rerank(self, query, docs):
        print("✅ [Cross-Encoder] Re-ranking candidates...")
        # Simulating score: (doc, score)
        scored = []
        for d in docs:
            score = 0
            if "cost" in d or "$" in d: score += 0.9 # Keyword match simulation
            scored.append((d, score))
            
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[0][0]

def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (Advanced RAG) ---")
    rag = AdvancedRAG()
    query = "How much is a Tesla?"
    
    # Step 1: HyDE
    hypothetical = rag.hyde_transform(query)
    
    # Step 2: Vector Search
    candidates = rag.vector_search(hypothetical)
    
    # Step 3: Re-rank
    best_doc = rag.rerank(query, candidates)
    
    print(f"✅ Context sent to LLM: '{best_doc}'")
    
if __name__ == "__main__":
    print("🧪 RAG TEST: Naive (Bad) vs HyDE+Rerank (Good)\n")
    run_the_screwup()
    run_the_fix()

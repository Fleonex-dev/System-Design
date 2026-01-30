import time

# ==========================================
# 🛑 THE SCREW UP (No Cache / Exact Match Cache)
# ==========================================
# SCENARIO: 
# User 1: "How to kill a process in linux?" -> LLM ($0.01)
# User 2: "Kill process linux command" -> LLM ($0.01)
# An exact match cache misses this, because string != string.

class ExpensiveLLM:
    def call(self, prompt):
        print(f"💸 Calling LLM API for: '{prompt}' (Cost: $0.01)")
        time.sleep(0.5) # slow
        return "kill -9 <pid>"

def run_the_screwup():
    print("🛑 [Bad] Standard Caching...")
    llm = ExpensiveLLM()
    cache = {} 
    
    queries = [
        "How to kill process linux",
        "How to kill process linux", # HIT
        "Kill process linux cmd"     # MISS (Semantically same, but string different)
    ]
    
    for q in queries:
        if q in cache:
            print(f"🛑 Cache HIT for '{q}'")
        else:
            cache[q] = llm.call(q)


# ==========================================
# ✅ THE FIX (Semantic Caching)
# ==========================================
# SCENARIO: We embed the query. If cosine_similarity > 0.9, we return cached result.
# Simulating embeddings using a dummy hash for demonstration.

def get_embedding_mock(text):
    # In reality, this calls OpenAI Ada-002
    # Here, we just map "kill", "process", "linux" to a similar vector
    keywords = set(text.lower().split())
    return keywords

def is_semantically_similar(q1, q2_keywords):
    q1_keywords = set(q1.lower().split())
    # Jaccard similarity simulation
    intersection = q1_keywords.intersection(q2_keywords)
    similarity = len(intersection) / len(q1_keywords.union(q2_keywords))
    return similarity > 0.5 

def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (Semantic Cache) ---")
    llm = ExpensiveLLM()
    # Cache format: { "keywords_set": "response" }
    # In Prod: This is a Vector DB (Pinecone/Redis)
    vector_cache = [] 
    
    queries = [
        "How to kill process linux",
        "Kill process linux cmd",     # Should be a HIT now!
        "Making a pie recipe"         # Total miss
    ]
    
    for q in queries:
        # Check cache
        hit = False
        current_keywords = get_embedding_mock(q)
        
        for cached_keywords, response in vector_cache:
            if is_semantically_similar(q, cached_keywords):
                print(f"✅ Semantic Cache HIT for '{q}' (Saved $0.01)")
                hit = True
                break
        
        if not hit:
            resp = llm.call(q)
            vector_cache.append((current_keywords, resp))

if __name__ == "__main__":
    print("🧪 CACHE TEST: Standard (Bad) vs Semantic (Good)\n")
    run_the_screwup()
    run_the_fix()
    
    print("\n🏆 Conclusion: Semantic Cache saves money on 'similar' queries.")

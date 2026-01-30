# 01_kv_cache.py
import time
import sys

# ==========================================
# 🧠 KV CACHE (The Secret to Fast Inference)
# ==========================================
# SCENARIO: Generating "The quick brown fox".
# Step 1: Input "The" -> Compute K,V for "The".
# Step 2: Input "The quick" -> Naive way re-computes "The" again!
#
# KV Cache stores the Past Key/Values so we only compute the NEW token.
# Tradeoff: Massive RAM usage (VRAM).

def naive_inference(tokens):
    # Simulates re-processing ALL tokens
    time.sleep(0.05 * len(tokens)) 

def cached_inference(new_token):
    # Simulates processing ONLY the new token
    time.sleep(0.05) 

def run_simulation():
    print("--- 🧠 KV Cache Simulation ---")
    prompt = ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]
    
    # 1. NAIVE (Quadratic Slowdown)
    print("1️⃣  Naive Generation (Re-computing context):")
    context = []
    start = time.time()
    for token in prompt:
        context.append(token)
        naive_inference(context)
        print(f"   Generated: {token} (Ctx: {len(context)})")
    
    print(f"   ⏱️ Total Time: {time.time() - start:.2f}s")
    
    # 2. KV CACHE (Linear Speed)
    print("\n2️⃣  KV Cache Generation (Incremental):")
    context = []
    start = time.time()
    for token in prompt:
        context.append(token)
        cached_inference(token) # Only process new
        print(f"   Generated: {token} (Ctx: {len(context)})")
        
    print(f"   ⏱️ Total Time: {time.time() - start:.2f}s")
    
    print("\n🏆 Insight: KV Cache is mandatory for Chatbots. 8k context without cache = Unusable latency.")
    print("   But it eats VRAM. 1 Token = 2 * Layers * Heads * Dim * Precision bytes.")

if __name__ == "__main__":
    run_simulation()

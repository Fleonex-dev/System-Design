# 03_inference_optimization.py
import time
import random

# ==========================================
# 🛑 THE SCREW UP (Standard Autoregressive decoding)
# ==========================================
# SCENARIO: Generating 5 tokens.
# Big Model takes 0.1s per token.
# Total time = 0.5s.
# We process each token serially because we need the previous one to predict the next.

class BigModel:
    def predict_one(self, context):
        time.sleep(0.1) # Simulate Heavy Compute
        return "token"

def run_the_screwup():
    print("🛑 [Bad] Standard Decoding (Serial)...")
    model = BigModel()
    start = time.time()
    
    generated = []
    for _ in range(5):
        token = model.predict_one(generated)
        generated.append(token)
        print(".", end="", flush=True)
        
    print(f"\n🛑 Total Time: {time.time() - start:.2f}s (Expected ~0.5s)")


# ==========================================
# ✅ THE FIX (Speculative Decoding)
# ==========================================
# SCENARIO: 
# 1. Use a Draft Model (Tiny, 0.01s latency) to guess 5 tokens ahead.
# 2. Ask Big Model to VERIFY them all at once (Parallel).
# 3. If Big Model agrees with the first 3 drafts, we accept them!
#    We got 3 tokens for the price of 1 Big Model call.

class DraftModel:
    def predict_fast(self, k=5):
        time.sleep(0.01 * k) # Fast!
        # Simulating it being correct 80% of the time
        return ["token", "token", "token", "WRONG", "token"]

class BigModelParallel:
    def verify_batch(self, drafts):
        time.sleep(0.1) # Process batch in same time as single token!
        # Verification logic (Simulated)
        results = [True, True, True, False, True] # 4th one is rejected
        return results

def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (Speculative Decoding) ---")
    draft_model = DraftModel()
    big_model = BigModelParallel()
    
    start = time.time()
    
    # Step 1: Draft
    print("✅ Drafting 5 tokens...")
    drafts = draft_model.predict_fast(5)
    
    # Step 2: Verify in Parallel
    print("✅ Verifying batch...")
    checks = big_model.verify_batch(drafts)
    
    # Step 3: Accept/Reject
    accepted = []
    for token, is_valid in zip(drafts, checks):
        if is_valid:
            accepted.append(token)
        else:
            break # Stop at first error
            
    print(f"✅ Accepted {len(accepted)} tokens: {accepted}")
    print(f"✅ Total Time: {time.time() - start:.2f}s (Expected ~0.15s)")
    print("✅ Speedup: ~3x faster!")

if __name__ == "__main__":
    print("🧪 SPEED TEST: Serial (Bad) vs Speculative (Good)\n")
    run_the_screwup()
    run_the_fix()
    
    print("\n🏆 Conclusion: Speculative decoding allows 3x-5x speedups in production.")

# 06_token_bucket.py
import time
import threading

# ==========================================
# 🪣 TOKEN BUCKET (Rate Limiter Algorithm)
# ==========================================
# SCENARIO: Allow 5 requests per second.
# Burst allowed? Yes (Bucket size).
#
# Logic: A "Refiller" adds tokens to the bucket every second.
# Request: Attempts to take a token. If empty -> 429 Too Many Requests.

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate # Tokens per second
        self.last_refill = time.time()
        self.lock = threading.Lock()
        
    def _refill(self):
        now = time.time()
        delta = now - self.last_refill
        new_tokens = delta * self.refill_rate
        
        if new_tokens > 0:
            self.tokens = min(self.capacity, self.tokens + new_tokens)
            self.last_refill = now
            
    def consume(self, tokens=1):
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True # Allowed
            return False # Denied

def run_simulation():
    print("--- 🪣 Token Bucket Demo ---")
    # Cap 5, Refill 1 per sec
    bucket = TokenBucket(capacity=5, refill_rate=1)
    
    # 1. Burst (5 requests) -> Should succeed
    print("🔥 Bursting 5 requests...")
    for i in range(5):
        if bucket.consume(): print(f"   ✅ Req {i+1}: Allowed")
        else: print(f"   ❌ Req {i+1}: Rate Limited")
        
    # 2. Overload -> Should fail
    print("🚫 Bursting 6th request (Bucket empty)...")
    if bucket.consume(): print("   ✅ Req 6: Allowed")
    else: print("   ❌ Req 6: Rate Limited (Expected)")
    
    # 3. Wait for refill
    print("💤 Waiting 2 seconds (Refill 2 tokens)...")
    time.sleep(2)
    
    if bucket.consume(): print("   ✅ Req 7: Allowed (Refilled)")
    
    print("\n🏆 Insight: Token Bucket allows bursts (unlike Leaky Bucket).")
    print("   🏢 Real World: **Stripe** API, **Uber** driver matching, **AWS** API Throttling.")

if __name__ == "__main__":
    run_simulation()

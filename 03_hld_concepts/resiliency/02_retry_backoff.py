# 02_retry_backoff.py
import time
import random

# ==========================================
# 🔄 RETRY, BACKOFF & JITTER
# ==========================================
# SCENARIO: Transient failure.
# 1. Immediate Retry: SPAMs the server. "Thundering Herd".
# 2. Exponential Backoff: Wait 1s, 2s, 4s... (Better)
# 3. Jitter: Wait 1.1s, 1.9s, 4.3s... (Best - Decouples clients)

def call_service():
    if random.random() < 0.8:
        print("   ❌ 503 Service Unavailable")
        return False
    print("   ✅ 200 OK")
    return True

def retry_logic(strategy="jitter"):
    print(f"\n--- Strategy: {strategy.upper()} ---")
    attempts = 0
    max_retries = 5
    base_delay = 0.5
    
    while attempts < max_retries:
        attempts += 1
        print(f"Attempt {attempts}...", end="")
        
        if call_service():
            return
            
        # Calc Delay
        if strategy == "immediate":
            delay = 0.5
        elif strategy == "exponential":
            delay = base_delay * (2 ** (attempts - 1))
        elif strategy == "jitter":
            # Exo + Randomness
            expo = base_delay * (2 ** (attempts - 1))
            delay = expo + random.uniform(0, 0.5)
            
        print(f"   💤 Sleeping {delay:.2f}s...")
        time.sleep(delay)
        
    print("💀 Giving Up.")

if __name__ == "__main__":
    retry_logic("immediate")
    retry_logic("exponential")
    retry_logic("jitter")
    print("\n🏆 Rule: ALWAYS add Jitter to backoff to prevent Thundering Herd.")

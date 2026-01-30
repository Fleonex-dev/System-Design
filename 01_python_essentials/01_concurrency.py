import time
import asyncio
import requests # The blocking library (Bad for high concurrency)
import aiohttp  # The async library (Good for high concurrency)

# ==========================================
# 🛑 THE SCREW UP (Blocking/Sync)
# ==========================================
# SCENARIO: You are fetching responses from 3 LLM providers.
# In a synchronous world, you wait for one to finish before starting the next.
# If OpenAI takes 2s, Anthropic takes 2s, and Local takes 2s...
# Total time = 6s. This is UNACCEPTABLE for user-facing apps.

def fetch_sync(url):
    print(f"🛑 [Sync] Requesting {url}...")
    # This BLOCKS the entire program. Nothing else can happen.
    resp = requests.get(url)
    print(f"🛑 [Sync] Received from {url}")
    return resp.status_code

def run_the_screwup():
    print("\n--- 🛑 Running BAD implementation (Sync) ---")
    start = time.time()
    
    # We are calling a dummy API that delays response
    urls = [
        "https://httpbin.org/delay/1", # Simulate 1s latency
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1"
    ]
    
    for url in urls:
        fetch_sync(url)
        
    print(f"🛑 Total Sync Time: {time.time() - start:.2f}s (Expected: ~3.0s)")


# ==========================================
# ✅ THE FIX (Non-blocking/Async)
# ==========================================
# SCENARIO: We fire all requests at the same time.
# The CPU sits idle while waiting for network packets.
# Total time = Max(individual_latencies) = ~1s.

async def fetch_async(session, url):
    print(f"✅ [Async] Requesting {url}...")
    async with session.get(url) as response:
        print(f"✅ [Async] Received from {url}")
        return await response.read()

async def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (Async) ---")
    start = time.time()
    
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1"
    ]
    
    # Connector limit prevents frying your DNS
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_async(session, url) for url in urls]
        # gather fires them all at once and waits for all to land
        await asyncio.gather(*tasks)
        
    print(f"✅ Total Async Time: {time.time() - start:.2f}s (Expected: ~1.1s)")


if __name__ == "__main__":
    print("🧪 CONCURRENCY TEST: Sync (Bad) vs Async (Good)")
    print("Note: We are hitting httpbin.org which simulates network delay.")
    
    run_the_screwup()
    
    # Running async loop
    asyncio.run(run_the_fix())
    
    print("\n🏆 Conclusion: Async is O(1) relative to request count (mostly), Sync is O(N).")

import asyncio
import time

# ==========================================
# 🛑 THE SCREW UP (Blocking the Event Loop)
# ==========================================
# SCENARIO: You are using `asyncio` but you call `time.sleep()`.
# This freezes the ENTIRE loop. No other task can run.
# "Async" becomes "Sequential + Overhead".

async def blocking_task(name):
    print(f"🛑 [{name}] Start (Blocking)...")
    time.sleep(1) # EVIL!
    print(f"🛑 [{name}] Done.")

async def run_screwup():
    print("--- 🛑 Running Blocking Async ---")
    start = time.time()
    # These will run sequentially because t1 blocks the loop
    await asyncio.gather(
        blocking_task("A"),
        blocking_task("B")
    )
    print(f"🛑 Total Time: {time.time() - start:.2f}s (Expected ~1.0s if async)")

# ==========================================
# ✅ THE FIX (Non-blocking Yield)
# ==========================================
# SCENARIO: Use `await asyncio.sleep()`.
# This yields control back to the loop ("I'm waiting, you go ahead").
# Other tasks run immediately.

async def non_blocking_task(name):
    print(f"✅ [{name}] Start...")
    await asyncio.sleep(1) # Good!
    print(f"✅ [{name}] Done.")

async def run_fix():
    print("\n--- ✅ Running True Async ---")
    start = time.time()
    await asyncio.gather(
        non_blocking_task("A"),
        non_blocking_task("B")
    )
    print(f"✅ Total Time: {time.time() - start:.2f}s")

if __name__ == "__main__":
    asyncio.run(run_screwup())
    asyncio.run(run_fix())
    
    print("\n🏆 Lesson: Never call sync blocking functions (requests, time.sleep) inside async def.")

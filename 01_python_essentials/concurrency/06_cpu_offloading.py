import asyncio
import time
import concurrent.futures

# ==========================================
# 🛑 THE SCREW UP (Blocking the Main Thread)
# ==========================================
# SCENARIO: You serve 1000 users. One user asks to calculte Factorial(1000000).
# You run this on the main event loop.
# RESULT: Heartbeat fails. Health check fails. Deployment restarts. Outage.

def blocking_cpu_heavy_task(n):
    print(f"🛑 [CPU] Calculating factorial({n})... this freezes the loop!")
    # Simulate heavy work
    time.sleep(2) 
    return "Result: Big Number"

async def unrelated_quick_task():
    for i in range(5):
        print(f"   [ChatBot] Handling user request {i}...")
        await asyncio.sleep(0.3)

async def run_screwup():
    print("--- 🛑 Scenario: CPU Work on Main Thread ---")
    # This will NOT run in parallel. The quick task waits for the CPU task.
    await asyncio.gather(
        asyncio.to_thread(blocking_cpu_heavy_task, 10), # Still blocking if not handled right
        unrelated_quick_task()
    )

# ==========================================
# ✅ THE FIX (ProcessPoolExecutor)
# ==========================================
# SCENARIO: Offload the heavy math to a separate CPU Core.
# The Main Loop stays free to answer heartbeat/user requests.

def clean_cpu_task(n):
    # This runs in a separate process
    time.sleep(2)
    return f"Factorial({n}) Done"

async def run_fix():
    print("\n--- ✅ Scenario: Offloading to Process Pool ---")
    loop = asyncio.get_running_loop()
    
    # Create a separate process
    with concurrent.futures.ProcessPoolExecutor() as pool:
        # submit task to pool
        cpu_future = loop.run_in_executor(pool, clean_cpu_task, 100)
        
        # While that computes, our chat bot output keeps flowing FLUENTLY
        await unrelated_quick_task()
        
        result = await cpu_future
        print(f"✅ [Result] {result}")

if __name__ == "__main__":
    # We skip screwup for better demo speed, but logic holds.
    # asyncio.run(run_screwup()) 
    asyncio.run(run_fix())
    
    print("\n🏆 Rule: If it takes > 1ms of CPU, put it in a ProcessPool / ThreadPool.")

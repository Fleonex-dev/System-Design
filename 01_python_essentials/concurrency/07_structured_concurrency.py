import asyncio
import sys

# ==========================================
# 🛑 THE SCREW UP (Fire and Forget / Gather bugs)
# ==========================================
# SCENARIO: You spawn 10 tasks. Task 3 fails.
# `asyncio.gather` propagates the error, BUT Task 4, 5, 6 keep running in background (Zombies).
# They might consume resources or corrupt DB.

async def risky_task(id, delay, fail=False):
    try:
        print(f"   [Task {id}] working...")
        await asyncio.sleep(delay)
        if fail:
            raise Exception(f"Task {id} BOOM!")
        print(f"   [Task {id}] done.")
    except asyncio.CancelledError:
        print(f"   [Task {id}] was CANCELLED (Cleanup)")
        raise

async def run_screwup():
    print("--- 🛑 Scenario: Standard Gather (Leak) ---")
    try:
        await asyncio.gather(
            risky_task(1, 1),
            risky_task(2, 0.5, fail=True), # Fails fast
            risky_task(3, 2) # Will keep running technically unless explicitly cancelled
        )
    except Exception as e:
        print(f"🛑 Error Caught: {e}")
        # Task 3 is actually still running in background here in some versions!
        await asyncio.sleep(1.5) 
        print("🛑 Task 3 might have finished silently.")

# ==========================================
# ✅ THE FIX (TaskGroups - Python 3.11+)
# ==========================================
# SCENARIO: Usage of `asyncio.TaskGroup`.
# A Context Manager that guarantees: "If one fails, CANCEL ALL OTHERS immediately".
# No zombies. Safe shutdown.

async def run_fix():
    if sys.version_info < (3, 11):
        print("⚠️  Python 3.11+ required for TaskGroups.")
        return

    print("\n--- ✅ Scenario: TaskGroup (Structured) ---")
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(risky_task(1, 1))
            tg.create_task(risky_task(2, 0.5, fail=True)) # Dies
            tg.create_task(risky_task(3, 2)) # Should be cancelled immediately
            
    except ExceptionGroup as eg:
        print(f"✅ Caught ExceptionGroup. All other tasks were cancelled cleanly.")

if __name__ == "__main__":
    asyncio.run(run_screwup())
    # TaskGroup prevents the mess
    asyncio.run(run_fix())
    
    print("\n🏆 Structured Concurrency: 'No child left behind'.")

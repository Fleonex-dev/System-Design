# 00_intro_async.py
import asyncio
import time

# ==========================================
# ⚡ ASYNC 101: COROUTINES
# ==========================================
# 1. `async def` defines a COROUTINE.
# 2. Calling it DOES NOT run it. It returns a wrapper.
# 3. You must `await` it or run it in an Event Loop.

async def say_hello(name, delay):
    print(f"   👋 [{name}] Waiting {delay}s...")
    # await pauses THIS function, yielding control back to the loop
    await asyncio.sleep(delay) 
    print(f"   ✅ [{name}] Hello!")
    return f"Result from {name}"

async def main():
    print("--- 1. Defining Coroutines ---")
    # This creates the object, doesn't run execution
    coro = say_hello("Test", 1)
    print(f"Object type: {type(coro)}")
    print("Did anything print? No.")
    
    # We must await it to run it
    print("\n--- 2. Awaiting Execution ---")
    result = await coro
    print(f"Returned: {result}")
    
    print("\n--- 3. Concurrency (Gather) ---")
    print("Running 3 greetings AT ONCE...")
    start = time.time()
    
    # Schedule 3 tasks effectively in parallel (interleaved)
    await asyncio.gather(
        say_hello("Alice", 1.0),
        say_hello("Bob", 1.0),
        say_hello("Charlie", 1.0)
    )
    
    # Total time should be ~1s, not 3s
    print(f"Total Time: {time.time() - start:.2f}s")

if __name__ == "__main__":
    # Entry point for async programs
    asyncio.run(main())

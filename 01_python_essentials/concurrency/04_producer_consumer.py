import asyncio
import random
import time

# ==========================================
# 🛑 THE SCREW UP (Unbounded Growth)
# ==========================================
# SCENARIO: Producer is faster than Consumer.
# It keeps appending to a list.
# Memory grows until crash (OOM).

async def bad_producer(queue_list):
    while True:
        queue_list.append("item")
        if len(queue_list) > 10_000_000: # Simulating crash
            raise MemoryError("🔥 OOM Crash!")
        await asyncio.sleep(0.0001) # Fast

async def bad_consumer(queue_list):
    while True:
        if queue_list:
            queue_list.pop(0)
        await asyncio.sleep(0.1) # Slow

# ==========================================
# ✅ THE FIX (Async Queue + Backpressure)
# ==========================================
# SCENARIO: `asyncio.Queue(maxsize=10)`.
# If queue is full, `await queue.put()` BLOCKS the Producer.
# The Producer automatically slows down to match Consumer speed.
# This is called "Backpressure".

async def producer(queue, pid):
    for i in range(5):
        await queue.put(f"Item {i} from {pid}")
        print(f"   [P{pid}] Produced Item {i} (Q size: {queue.qsize()})")
        # No sleep needed, queue controls speed!

async def consumer(queue):
    while True:
        item = await queue.get()
        print(f"✅ [Consumer] Processing {item}...")
        await asyncio.sleep(0.5) # Simulating Slow IO
        queue.task_done()

async def run_fix():
    print("\n--- ✅ Running Producer-Consumer (Backpressure) ---")
    # Max buffer of 2 items
    q = asyncio.Queue(maxsize=2)
    
    # Start Consumer
    c_task = asyncio.create_task(consumer(q))
    
    # Start Producers
    await asyncio.gather(
        producer(q, 1),
        producer(q, 2)
    )
    
    print("✅ All items produced. Waiting for consumer to finish...")
    await q.join() # Wait for consumer to empty queue
    c_task.cancel() # Stop the infinite consumer loop

if __name__ == "__main__":
    try:
        # We don't run bad_producer here as it crashes the machine/script
        print("🛑 Bad producer (Unbounded list) would cause OOM.")
        
        asyncio.run(run_fix())
    except KeyboardInterrupt:
        pass
    
    print("\n🏆 Queue Backpressure prevents system overload.")

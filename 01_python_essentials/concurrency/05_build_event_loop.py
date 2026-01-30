import collections
import time
import random

# ==========================================
# 🧠 UNDER THE HOOD: THE EVENT LOOP
# ==========================================
# AsyncIO is NOT magic. It does not use "Parallelism".
# It uses "Cooperative Multitasking".
#
# Core Concept:
# 1. Tasks are just Generators (functions with `yield`).
# 2. The "Event Loop" is just a `while` loop that calls `next(task)`.
# 3. If a task is waiting (e.g., IO), it `yields` control back to the loop.
# 4. The loop runs the next task in the queue.

class SimpleEventLoop:
    def __init__(self):
        self.queue = collections.deque()
        
    def add_task(self, generator):
        self.queue.append(generator)
        
    def run(self):
        print("🔄 [Loop] Starting Event Loop...")
        while self.queue:
            task = self.queue.popleft() 
            
            try:
                # Run the task until it yields
                # This corresponds to "CPU slice" time
                status = next(task)
                
                # If task yields "waiting", we put it back at the end
                # (Round Robin scheduling)
                print(f"   [Loop] Task yielded: {status}")
                self.queue.append(task)
                
            except StopIteration:
                # Task finished
                print("   [Loop] Task Finished!")

def task_one():
    print("⚡ [Task 1] Start")
    yield "waiting for network..."
    print("⚡ [Task 1] Step 2")
    yield "waiting for DB..."
    print("⚡ [Task 1] Done")

def task_two():
    print("🔥 [Task 2] Start")
    yield "waiting for user..."
    print("🔥 [Task 2] Done")

if __name__ == "__main__":
    loop = SimpleEventLoop()
    
    # Schedule tasks
    loop.add_task(task_one())
    loop.add_task(task_two())
    
    # Run
    loop.run()
    
    print("\n🏆 Insight: Notice how Task 1 and 2 are INTERLEAVED?")
    print("   They run on the SAME thread. 'await' is basically Just 'yield'.")

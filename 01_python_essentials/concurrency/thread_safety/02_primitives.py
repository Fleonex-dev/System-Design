# 02_primitives.py
import threading
import time
import random

# ==========================================
# 🛠️ THREADING PRIMITIVES
# ==========================================

# 1. LOCK (Mutex)
# Use when 1 thread needs exclusive access.
lock = threading.Lock()
shared_resource = 0

def lock_demo():
    print("\n--- 🔒 LOCK (Mutex) ---")
    def safe_increment():
        global shared_resource
        with lock: # Critical Section
            current = shared_resource
            time.sleep(0.001)
            shared_resource = current + 1
            
    ts = [threading.Thread(target=safe_increment) for _ in range(100)]
    for t in ts: t.start()
    for t in ts: t.join()
    print(f"Result: {shared_resource} (Safe)")

# 2. RLOCK (Recursive Lock)
# Use when a function calls another function that ALSO needs the lock.
# A normal Lock would deadlock itself.
rlock = threading.RLock()

def rlock_demo():
    print("\n--- 🔄 RLOCK (Recursive) ---")
    def recursive_task(count):
        with rlock:
            if count <= 0: return
            print(f"   Enter Level {count}")
            recursive_task(count - 1) # Calls itself, re-acquiring lock
            
    recursive_task(3)
    print("✅ Recursion finished without deadlock.")

# 3. SEMAPHORE (Capacity)
# Use to limit concurrency (e.g., Max 3 DB connections).
sem = threading.Semaphore(2) # Max 2 threads

def semaphore_demo():
    print("\n--- 🚦 SEMAPHORE (Limit 2) ---")
    def restricted_task(id):
        with sem:
            print(f"   🟢 [T{id}] Acquired!")
            time.sleep(0.5)
            print(f"   ⚪ [T{id}] Released.")
            
    ts = [threading.Thread(target=restricted_task, args=(i,)) for i in range(5)]
    for t in ts: t.start()
    for t in ts: t.join()

# 4. EVENT (Signaling)
# Use to signal "Ready" state between threads.
start_flag = threading.Event()

def event_demo():
    print("\n--- 🏳️ EVENT (Signal) ---")
    def runner(id):
        print(f"   🏃 [Runner {id}] Waiting for gun...")
        start_flag.wait() # Blocks until set()
        print(f"   💨 [Runner {id}] GO!")
        
    ts = [threading.Thread(target=runner, args=(i,)) for i in range(3)]
    for t in ts: t.start()
    
    time.sleep(1)
    print("   🔫 BANG! (Setting Event)")
    start_flag.set()
    for t in ts: t.join()

if __name__ == "__main__":
    lock_demo()
    rlock_demo()
    semaphore_demo()
    event_demo()

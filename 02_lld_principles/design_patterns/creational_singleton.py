# 03_singleton_thread_safe.py
import threading
import time

# ==========================================
# 🔒 THREAD-SAFE SINGLETON
# ==========================================
# Scenario: Database Connection Pool.
# You want only ONE instance.
# Naive "if not instance: create()" is NOT thread-safe.
# Multiple threads might enter the `if` block simultaneously.

class Singleton:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        # 1. First Check (Fast, No Lock)
        # If already exists, return immediately.
        if not cls._instance:
            
            # 2. Acquire Lock (Slow, Safety)
            with cls._lock:
                # 3. Double Check (Crucial!)
                # Another thread might have created it while we waited for lock.
                if not cls._instance:
                    print("✨ Creating New Instance (Expensive)!")
                    cls._instance = super(Singleton, cls).__new__(cls)
                    # Simulate expensive init
                    time.sleep(0.1) 
                    
        return cls._instance

def test_concurrency():
    print("--- 🔒 Double-Checked Locking Test ---")
    instances = []
    
    def get_singleton():
        inst = Singleton()
        instances.append(inst)
        
    # Hammer it with 10 threads
    threads = [threading.Thread(target=get_singleton) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    first = instances[0]
    all_same = all(i is first for i in instances)
    
    print(f"Created {len(instances)} references.")
    if all_same:
        print("✅ SUCCESS: All references point to same object.")
    else:
        print("❌ FAILURE: Multiple objects created!")

if __name__ == "__main__":
    test_concurrency()

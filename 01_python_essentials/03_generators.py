import sys
import time

# ==========================================
# 🛑 THE SCREW UP (Eager Loading / Lists)
# ==========================================
# SCENARIO: You are reading a massive CSV file (e.g., 10GB log file).
# You try to load it all into a list.
# Result: Your server runs out of RAM (OOM) and crashes.

def get_logs_bad(n):
    print(f"🛑 [Bad] Eagerly creating list of {n} items...")
    # This creates the ENTIRE list in memory immediately.
    # [0, 1, 4, 9, 16, ...]
    return [i * i for i in range(n)]

def run_the_screwup():
    print("\n--- 🛑 Running BAD implementation (Lists) ---")
    
    # We use 10,000,000 to simulate a big dataset
    N = 10_000_000
    
    try:
        start = time.time()
        data = get_logs_bad(N)
        end = time.time()
        
        # Check memory usage
        size_bytes = sys.getsizeof(data)
        print(f"🛑 Time to load: {end - start:.4f}s")
        print(f"🛑 Memory Used: {size_bytes / 1024 / 1024:.2f} MB")
        
        # Simulating processing
        # for x in data: pass
        
    except MemoryError:
        print("🛑 SYSTEM CRASHED: Out of Memory!")


# ==========================================
# ✅ THE FIX (Generators / Lazy Loading)
# ==========================================
# SCENARIO: You process one line at a time.
# "yield" pauses the function and saves its state.
# RAM usage stays constant (almost 0), no matter how big the file is.

def get_logs_good(n):
    print(f"✅ [Good] Lazily yielding {n} items...")
    # This yields one item at a time. It NEVER builds a list.
    for i in range(n):
        yield i * i

def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (Generators) ---")
    
    N = 10_000_000
    
    start = time.time()
    # Notice: Calling the function does NOTHING yet. It just returns a generator object.
    generator = get_logs_good(N)
    
    # Check memory usage of the generator object itself
    size_bytes = sys.getsizeof(generator)
    print(f"✅ Memory Used (Generator Object): {size_bytes} BYTES (Not MB!)")
    
    # Process items
    count = 0
    for item in generator:
        count += 1
        # In real life, we would send this 'item' to the user immediately (Streaming)
        if count == 1:
            print("✅ First item processed immediately!")
            
    print(f"✅ Finished processing {count} items.")
    print(f"✅ Total Time: {time.time() - start:.4f}s")


if __name__ == "__main__":
    print("🧪 GENERATORS TEST: OOM (Bad) vs Streaming (Good)\n")
    
    # Warning: Bad might use ~400MB RAM. Ensure your system can handle it.
    run_the_screwup()
    
    run_the_fix()
    
    print("\n🏆 Conclusion: Generators use O(1) Memory. Lists use O(N).")

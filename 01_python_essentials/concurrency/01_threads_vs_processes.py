import time
import threading
import multiprocessing
import os

# ==========================================
# 🛑 THE SCREW UP (Using Threads for CPU Work)
# ==========================================
# SCENARIO: You are calculating Primes (CPU Bound).
# You assume Threads will make it faster by using multiple cores.
# REALITY: The GIL (Global Interpreter Lock) ensures only ONE thread runs Python bytecode at a time.
# Result: Context Switching overhead makes it SLOWER than serial.

def cpu_heavy_task(n):
    count = 0
    while count < n:
        count += 1
    return count

def run_threads():
    print("🛑 [Threads] Starting 2 CPU heavy tasks...")
    start = time.time()
    n = 50_000_000
    
    t1 = threading.Thread(target=cpu_heavy_task, args=(n,))
    t2 = threading.Thread(target=cpu_heavy_task, args=(n,))
    
    t1.start(); t2.start()
    t1.join(); t2.join()
    
    print(f"🛑 [Threads] Time: {time.time() - start:.2f}s (GIL blocked parallelism)")

# ==========================================
# ✅ THE FIX (Using Processes)
# ==========================================
# SCENARIO: `multiprocessing` spawns a fresh Python interpreter for each task.
# Each has its own GIL. True Parallelism on multicore CPUs.

def run_processes():
    print("✅ [Processes] Starting 2 CPU heavy tasks...")
    start = time.time()
    n = 50_000_000
    
    p1 = multiprocessing.Process(target=cpu_heavy_task, args=(n,))
    p2 = multiprocessing.Process(target=cpu_heavy_task, args=(n,))
    
    p1.start(); p2.start()
    p1.join(); p2.join()
    
    print(f"✅ [Processes] Time: {time.time() - start:.2f}s (True Parallelism)")

if __name__ == "__main__":
    print(f"🧪 CPU: {os.cpu_count()} Cores available.")
    print("--- COMPARISON ---")
    
    # 1. Serial (Baseline)
    start = time.time()
    cpu_heavy_task(50_000_000)
    cpu_heavy_task(50_000_000)
    print(f"🐢 [Serial] Time: {time.time() - start:.2f}s")
    
    run_threads()
    run_processes()
    
    print("\n🏆 Rule of Thumb: Use Threads for I/O (Network/Disk). Use Processes for CPU (Math/Data).")

# 00_intro_multiprocessing.py
import multiprocessing
import time
import os

# ==========================================
# 🏭 MULTIPROCESSING 101: ISOLATION
# ==========================================
# CONCEPT: A Process has its own MEMORY SPACE.
# Variables are NOT shared.
# If Child changes 'X', Parent sees old 'X'.

# Global Variable
shared_data = []

def child_worker(name):
    print(f"   👶 [Child-{name}] PID: {os.getpid()}")
    print(f"   👶 [Child-{name}] Modifying Shared Data...")
    shared_data.append(f"Data from {name}")
    print(f"   👶 [Child-{name}] My Data: {shared_data}")

def run_demo():
    print(f"👨 [Parent] PID: {os.getpid()}")
    print(f"👨 [Parent] Initial Data: {shared_data}")
    
    p1 = multiprocessing.Process(target=child_worker, args=("A",))
    p1.start()
    p1.join()
    
    print("\n--- 🕵️ MEMORY CHECK ---")
    print(f"👨 [Parent] Data after Child finished: {shared_data}")
    
    if len(shared_data) == 0:
        print("✅ PROOF: Parent data is EMPTY. Child modified its OWN copy.")
    else:
        print("❌ ERROR: Memory was shared (Impossible in standard MP).")

if __name__ == "__main__":
    # Windows/macOS require this guard
    run_demo()

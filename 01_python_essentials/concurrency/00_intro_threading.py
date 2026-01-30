# 00_intro_threading.py
import threading
import time
import os

# ==========================================
# 🧵 THREADING 101: LIFECYCLE
# ==========================================
# CONCEPT: A Thread is a separate flow of execution within the SAME Process.
# They SHARE memory (Global variables).

def print_numbers(name):
    print(f"   [T-{name}] Starting...")
    for i in range(3):
        time.sleep(0.5) # Simulate work
        print(f"   [T-{name}] Count {i}")
    print(f"   [T-{name}] Done.")

def run_demo():
    print(f"🤖 [Main] Process PID: {os.getpid()}")
    print("--- 1. Creating Threads ---")
    
    # 1. Creation: Pass target function and arguments
    t1 = threading.Thread(target=print_numbers, args=("Alice",))
    t2 = threading.Thread(target=print_numbers, args=("Bob",))
    
    # 2. Start: Actually launches the OS thread
    print("🤖 [Main] Starting Threads...")
    t1.start()
    t2.start()
    
    print("🤖 [Main] Threads are running in background...")
    print("🤖 [Main] Doing Main Thread work...")
    
    # 3. Join: Wait for them to finish
    # If we don't join, the script might exit while threads are still running 
    # (unless they are Daemon threads).
    t1.join()
    t2.join()
    
    print("--- 2. Daemon Threads ---")
    # Daemon threads die instantly when the Main program exits.
    # Useful for background tasks (heartbeats, loggers).
    d = threading.Thread(target=print_numbers, args=("Daemon",), daemon=True)
    d.start()
    print("🤖 [Main] Exiting (Daemon will be killed instantly)...")

if __name__ == "__main__":
    run_demo()

# 01_race_condition_threading.py
import threading
import time
import dis

# ==========================================
# 🛑 THE RACE CONDITION
# ==========================================
# SCENARIO: `counter += 1` looks like 1 line of code.
# In Assembly/Bytecode, it is 3 steps:
# 1. LOAD_FAST (Read value)
# 2. BINARY_ADD (Add 1)
# 3. STORE_FAST (Write back)
#
# A Context Switch can happen between 1 and 3.
# Thread A reads 0. Thread B reads 0. Both write 1. Result: 1 (should be 2).

counter = 0

def worker(n):
    global counter
    for _ in range(n):
        counter += 1

def run_race():
    global counter
    counter = 0
    print("--- 🛑 Race Condition Test ---")
    
    t1 = threading.Thread(target=worker, args=(1_000_000,))
    t2 = threading.Thread(target=worker, args=(1_000_000,))
    
    t1.start(); t2.start()
    t1.join(); t2.join()
    
    print(f"Final Counter: {counter:,}")
    print(f"Expected:      2,000,000")
    
    if counter < 2_000_000:
        print("❌ Data Loss Detected! (Not atomic)")

def show_bytecode():
    print("\n--- 🧠 Bytecode Proof ---")
    def add_one():
        global x
        x += 1
    
    dis.dis(add_one)
    print("See? Read -> Add -> Write. Not Atomic.")

if __name__ == "__main__":
    run_race()
    show_bytecode()

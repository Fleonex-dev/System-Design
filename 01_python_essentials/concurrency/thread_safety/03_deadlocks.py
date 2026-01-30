# 03_deadlocks.py
import threading
import time
import random

# ==========================================
# 💀 DEADLOCK (Dining Philosophers)
# ==========================================
# Scenario: 5 Philosophers, 5 Forks.
# To eat, you need Left Fork AND Right Fork.
# If everyone grabs Right Fork, then waits for Left...
# DEADLOCK. Everyone waits forever.

forks = [threading.Lock() for _ in range(5)]

def philosopher(id, left_fork, right_fork):
    # DEADLOCK PRONE STRATEGY:
    # Always grab Left then Right.
    
    # ❌ THE PROBLEM: Cyclic Dependency.
    # P0 holds F0, wants F1
    # P1 holds F1, wants F2...
    # P4 holds F4, wants F0.
    
    # ✅ THE FIX: Resource Ordering.
    # Always grab lower index fork first, then higher index.
    first = left_fork if left_fork < right_fork else right_fork
    second = right_fork if first == left_fork else left_fork
    
    # Map index to Lock object
    first_lock = forks[first]
    second_lock = forks[second]
    
    while True:
        print(f"   🤔 [P{id}] Thinking...")
        with first_lock:
            print(f"   🥢 [P{id}] Picked {first}")
            time.sleep(0.1) # Simulate hesitation (danger zone)
            
            with second_lock:
                print(f"   🍝 [P{id}] EATING with {first}+{second}")
                time.sleep(0.5)
                print(f"   😋 [P{id}] Done.")
                break # Ate once, exit

def run_simulation():
    print("--- 💀 Dining Philosophers (Fixed) ---")
    threads = []
    for i in range(5):
        left = i
        right = (i + 1) % 5
        t = threading.Thread(target=philosopher, args=(i, left, right))
        threads.append(t)
        
    for t in threads: t.start()
    for t in threads: t.join()
    print("✅ Everyone ate. No Deadlock.")

if __name__ == "__main__":
    run_simulation()

import asyncio
import random

# ==========================================
# 🛑 THE SCREW UP (Race Condition)
# ==========================================
# SCENARIO: Two async tasks modifying a shared variable.
# While `+=` looks atomic, in complex objects or DBs it isn't.
# Even in Python async (single thread), context switches at `await` can cause issues.

class UnsafeBank:
    def __init__(self):
        self.balance = 0
        
    async def deposit(self, amount):
        # Specific simulation of "Read-Modify-Write" gap
        temp = self.balance
        await asyncio.sleep(0.001) # Force context switch
        self.balance = temp + amount

async def run_screwup():
    print("--- 🛑 Unsafe Bank (Race Condition) ---")
    bank = UnsafeBank()
    
    # 100 deposits of $1. Should be $100.
    tasks = [bank.deposit(1) for _ in range(100)]
    await asyncio.gather(*tasks)
    
    print(f"🛑 Final Balance: ${bank.balance} (Expected $100)")

# ==========================================
# ✅ THE FIX (Locks)
# ==========================================
# SCENARIO: Use `asyncio.Lock()`.
# Only one task can enter the `async with lock:` block.
# Others wait. Safe.

class SafeBank:
    def __init__(self):
        self.balance = 0
        self.lock = asyncio.Lock()
        
    async def deposit(self, amount):
        async with self.lock: # Critical Section
            temp = self.balance
            await asyncio.sleep(0.001)
            self.balance = temp + amount

async def run_fix():
    print("\n--- ✅ Safe Bank (Mutex Lock) ---")
    bank = SafeBank()
    
    tasks = [bank.deposit(1) for _ in range(100)]
    await asyncio.gather(*tasks)
    
    print(f"✅ Final Balance: ${bank.balance}")

if __name__ == "__main__":
    asyncio.run(run_screwup())
    asyncio.run(run_fix())
    
    print("\n🏆 Mutex Locks serialize access to shared state.")

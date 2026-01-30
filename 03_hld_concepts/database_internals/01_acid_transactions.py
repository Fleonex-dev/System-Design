# 01_acid_transactions.py
import threading
import time

# ==========================================
# 🏦 DATABASE INTERNALS: ACID
# ==========================================
# Scenario: Transfer $100 from Alice to Bob.
# We must ensure Atomicity: Either BOTH happen, or NEITHER.
# We must ensure Isolation: No one sees partial state.

class Database:
    def __init__(self):
        self.data = {"Alice": 1000, "Bob": 0}
        self.lock = threading.Lock()
        
    def get_balance(self, user):
        return self.data.get(user, 0)

    # 🛑 DIRTY READ (Unsafe)
    def transfer_unsafe(self, amount):
        # Step 1: Deduct
        self.data["Alice"] -= amount
        # ... Crash/Delay happens here ...
        time.sleep(0.1) # Window for dirty read
        # Step 2: Add
        self.data["Bob"] += amount

    # ✅ TRANSACTION (Safe)
    def transfer_safe(self, amount):
        with self.lock: # Act as Row Locks / Table Lock
            # Check constraints
            if self.data["Alice"] < amount:
                raise ValueError("Insufficient Funds")
                
            # Step 1
            self.data["Alice"] -= amount
            # Step 2
            self.data["Bob"] += amount

def run_simulation():
    db = Database()
    print("--- 🛑 Dirty Read Simulation ---")
    
    def auditor():
        time.sleep(0.05) # Check mid-transfer
        total = db.get_balance("Alice") + db.get_balance("Bob")
        print(f"   👀 [Auditor] Total Money: ${total}")
        if total < 1000:
            print("   ❌ MONEY DISAPPEARED! (Dirty Read)")
    
    t_transfer = threading.Thread(target=db.transfer_unsafe, args=(100,))
    t_audit = threading.Thread(target=auditor)
    
    t_transfer.start(); t_audit.start()
    t_transfer.join(); t_audit.join()
    
    print("\n--- ✅ ACID Transaction ---")
    db = Database() # Reset
    t_transfer = threading.Thread(target=db.transfer_safe, args=(100,))
    t_audit = threading.Thread(target=auditor)
    
    t_transfer.start(); t_audit.start()
    t_transfer.join(); t_audit.join()
    print("   (Auditor likely saw state before or after, but consistently total $1000)")

if __name__ == "__main__":
    run_simulation()

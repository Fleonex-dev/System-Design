# optimal.py
import threading

# ==========================================
# ✅ OPTIMAL: DATABASE LOCKING (ACID)
# ==========================================
# STRATEGY:
# 1. Pessimistic Lock: "SELECT * FROM seats WHERE id=1 FOR UPDATE"
# 2. Or Optimistic Lock: "UPDATE seats SET booked=1 WHERE id=1 AND booked=0"
#
# Here we simulate a Mutex (Lock) which acts like a Row Lock in Postgres.

class SafeSeatDB:
    def __init__(self):
        self.seats = 1
        self.lock = threading.Lock()
        
    def book(self, user):
        print(f"   👤 {user} requesting lock...")
        
        with self.lock: # <--- CRITICAL SECTION
            if self.seats > 0:
                print(f"   🎫 {user} BOOKED! (Safe)")
                self.seats -= 1
            else:
                print(f"   ❌ {user} Failed (Sold Out).")

def attempt_booking(db, user):
    db.book(user)

if __name__ == "__main__":
    db = SafeSeatDB()
    t1 = threading.Thread(target=attempt_booking, args=(db, "Alice"))
    t2 = threading.Thread(target=attempt_booking, args=(db, "Bob"))
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    print("\n🏆 Insight: High demand requires serialization.")
    print("   Postgres `FOR UPDATE` or Redis Distributed Locks are used here.")

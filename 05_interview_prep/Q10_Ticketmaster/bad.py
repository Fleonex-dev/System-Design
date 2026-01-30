# bad.py
import time
import threading

# ==========================================
# 🛑 BAD: RACE CONDITIONS (Double Booking)
# ==========================================
# SCENARIO: 1 Seat left for Taylor Swift. 2 Users click "Buy" at exact same time.
# NAIVE: Read availability -> Check > 0 -> Book.
# PROBLEM: Both read "1 seat available". Both book. Oversold.

class SeatDB:
    def __init__(self):
        self.seats = 1
        
    def book(self, user):
        print(f"   👤 {user} checking availability...")
        current = self.seats
        time.sleep(0.1) # Simulate DB latency
        
        if current > 0:
            print(f"   🎫 {user} BOOKED!")
            self.seats = current - 1
        else:
            print(f"   ❌ {user} Failed.")

def attempt_booking(db, user):
    db.book(user)

if __name__ == "__main__":
    db = SeatDB()
    t1 = threading.Thread(target=attempt_booking, args=(db, "Alice"))
    t2 = threading.Thread(target=attempt_booking, args=(db, "Bob"))
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    print(f"Remaining seats: {db.seats} (Should be 0, but might be -1 if buggy)")

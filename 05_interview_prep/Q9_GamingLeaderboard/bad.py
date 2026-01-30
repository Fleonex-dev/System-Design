# bad.py
import time

# ==========================================
# 🛑 BAD: RELATIONAL DB SORTING
# ==========================================
# SCENARIO: 10 Million Players. We need Top 10.
# NAIVE: "SELECT * FROM scores ORDER BY score DESC LIMIT 10"
#
# PROBLEM:
# 1. O(N log N) sort on every query.
# 2. DB CPU spikes to 100%.

class SQLDatabase:
    def __init__(self):
        self.rows = []
        
    def insert(self, player, score):
        self.rows.append({"p": player, "s": score})
        
    def get_top_10(self):
        print("   🐢 Scanning entire table to sort...")
        # Simulating slow sort
        self.rows.sort(key=lambda x: x["s"], reverse=True)
        return self.rows[:3]

if __name__ == "__main__":
    db = SQLDatabase()
    for i in range(1000): # Imagine 1 Million
        db.insert(f"User{i}", i)
        
    print(db.get_top_10())

# bad.py
import time

# ==========================================
# 🛑 BAD: BATCH PROCESSING FOR STREAM
# ==========================================
# SCENARIO: Ad Clicks coming in 1000/sec. Need real-time usage stats.
# NAIVE: Store individual clicks in DB. Run "COUNT(*)" every minute.
# PROBLEM: DB writes explode. Query is slow.

class Database:
    def __init__(self):
        self.rows = []
        
    def record_click(self, ad_id):
        # ❌ WRITING EVERY EVENT
        self.rows.append(ad_id) 
        
    def run_report(self):
        print(f"   🐢 Counting {len(self.rows)} rows...")
        return len(self.rows)

if __name__ == "__main__":
    db = Database()
    for _ in range(100): db.record_click("ad_1")
    
    print(f"Total: {db.run_report()}")

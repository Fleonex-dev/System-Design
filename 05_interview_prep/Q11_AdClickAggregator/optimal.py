# optimal.py
import time
from collections import defaultdict

# ==========================================
# ✅ OPTIMAL: WINDOWED AGGREGATION (Flink/Spark)
# ==========================================
# STRATEGY:
# 1. Aggregate in memory (Tumbling Window).
# 2. Flush only the COUNT to DB every 1 sec.
# 3. Handle late events (Watermarking).

class StreamProcessor:
    def __init__(self):
        self.window_counts = defaultdict(int)
        
    def process_event(self, ad_id):
        # ✅ AGGREGATING IN MEMORY
        self.window_counts[ad_id] += 1
        
    def flush_window(self):
        for ad_id, count in self.window_counts.items():
            print(f"   💾 Writing to DB: Ad {ad_id} = {count} clicks (1 Write)")
        self.window_counts.clear()

if __name__ == "__main__":
    print("--- ⚡ Real-time Stream Processing ---")
    proc = StreamProcessor()
    
    # 100 Clicks come in
    for _ in range(100): proc.process_event("ad_1")
    
    # End of Window
    proc.flush_window()
    
    print("\n🏆 Insight: BatchDB writes are dead. Use Stream Aggregation.")
    print("   Tech: **Apache Flink**, **Kafka Streams**, **Spark Streaming**.")

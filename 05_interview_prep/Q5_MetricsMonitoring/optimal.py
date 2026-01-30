# design_metrics.py
import time
import random

# ==========================================
# 📊 SYSTEM DESIGN: METRICS (Datadog)
# ==========================================
# CHALLENGES:
# 1. Write Heavy: 1M metrics/sec. Database will die on INSERT.
# 2. Aggregation: We don't need every millisecond. We need 1-min averages.
# 3. Retention: Keep raw data for 1 day, averages for 1 year (Downsampling).

class MetricsIngestor:
    def __init__(self):
        self.buffer = [] # Memory buffer
        
    def ingest(self, metric):
        # 1. Write to Memory Buffer (Fast)
        self.buffer.append(metric)
        
        # 2. Flush to Disk/DB in Batches
        if len(self.buffer) >= 5:
            self._flush()
            
    def _flush(self):
        print(f"   💾 [Batch Write] Flushed {len(self.buffer)} metrics to Time-Series DB (Cassandra/Influx).")
        # Simulate aggregation (Rollup)
        avg = sum(self.buffer) / len(self.buffer)
        print(f"   📉 [Rollup] Calculated 10s Average: {avg:.2f}")
        self.buffer = []

def run_simulation():
    print("--- 📊 Metrics System (Write Heavy) ---")
    agent = MetricsIngestor()
    
    # Simulate high volume traffic
    for i in range(12):
        val = random.randint(1, 100)
        print(f"   📥 Ingest: {val}")
        agent.ingest(val)
        time.sleep(0.1)
        
    print("\n🏆 Scale Tip: NEVER write 1-by-1 to DB. Always batch in memory or Kafka.")
    print("   🏢 Real World: **Datadog** uses Kafka -> S3/Cassandra. **Prometheus** uses a Pull model.")

if __name__ == "__main__":
    run_simulation()

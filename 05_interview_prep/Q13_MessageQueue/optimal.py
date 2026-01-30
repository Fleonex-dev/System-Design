# optimal.py
# ==========================================
# ✅ OPTIMAL: DISTRIBUTED LOG (Kafka)
# ==========================================
# STRATEGY:
# 1. Persistence: Append-only log file on disk.
# 2. Offsets: Consumers track "Where am I?".
# 3. Replayability: Reading doesn't delete.

class KafkaTopic:
    def __init__(self):
        self.log = [] # Represents Disk
        
    def append(self, msg):
        offset = len(self.log)
        self.log.append(msg)
        return offset
        
    def read(self, offset):
        if offset < len(self.log):
            return self.log[offset]
        return None

class ConsumerGroup:
    def __init__(self, topic, name):
        self.topic = topic
        self.name = name
        self.offset = 0
        
    def poll(self):
        msg = self.topic.read(self.offset)
        if msg:
            print(f"   [{self.name}] Read Offset {self.offset}: {msg}")
            self.offset += 1
        else:
            print(f"   [{self.name}] Up to date.")

if __name__ == "__main__":
    print("--- 📨 Kafka Design ---")
    topic = KafkaTopic()
    topic.append("Order 123")
    topic.append("Order 124")
    
    # Consumer A (Real-time)
    c1 = ConsumerGroup(topic, "Service A")
    c1.poll()
    c1.poll()
    
    # Consumer B (Analytics - Replay from start)
    print("\n⚠️ Service B starts late (Replay):")
    c2 = ConsumerGroup(topic, "Service B")
    c2.poll() # Reads Order 123 again!
    
    print("\n🏆 Insight: Kafka is not a Queue. It's a Log.")
    print("   This allows multiple consumers to read same data at different speeds.")

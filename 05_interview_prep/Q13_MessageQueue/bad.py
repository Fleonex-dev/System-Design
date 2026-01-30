# bad.py
import queue

# ==========================================
# 🛑 BAD: IN-MEMORY QUEUE
# ==========================================
# SCENARIO: Data Pipeline.
# NAIVE: Python `Queue`.
# PROBLEM: 
# 1. Non-persistent (Crash = Data Loss).
# 2. Cannot replay (Once popped, it's gone).
# 3. Hard to scale consumers.

class SimpleQueue:
    def __init__(self):
        self.q = queue.Queue()
        
    def produce(self, msg):
        self.q.put(msg)
        
    def consume(self):
        item = self.q.get()
        print(f"   😋 Consumed: {item}")
        # GONE FOREVER

if __name__ == "__main__":
    q = SimpleQueue()
    q.produce("Event 1")
    q.consume()

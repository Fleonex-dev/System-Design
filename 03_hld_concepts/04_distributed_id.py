import time
import threading

# ==========================================
# 🛑 THE SCREW UP (Auto Increment / Random)
# ==========================================
# SCENARIO: 
# Bad 1: "id = id + 1". Fails with multi-master DB (Collisions).
# Bad 2: "uuid.uuid4()". Too long (string), creates fragmentation in B-Tree index.

class BadIDGenerator:
    def __init__(self):
        self.id = 0
    def get_id(self):
        # NOT THREAD SAFE!
        self.id += 1
        return self.id

def run_the_screwup():
    print("🛑 [Bad] Auto-Increment...")
    gen = BadIDGenerator()
    # Simulating race condition
    # In real distributed systems, 2 servers might generate "1001" at same time
    print(f"🛑 Generated: {gen.get_id()} (Need Sync locks or DB coordination)")


# ==========================================
# ✅ THE FIX (Snowflake ID)
# ==========================================
# SCENARIO: 64-bit integer.
# 1 bit (unused) + 41 bits (Timestamp) + 10 bits (MachineID) + 12 bits (Sequence).
# Sortable by time. Unique across machines. Fits in 'bigint'.

class SnowflakeGenerator:
    def __init__(self, worker_id, datacenter_id):
        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = 0
        self.last_timestamp = -1
        
        # Bit offsets
        self.seq_bits = 12
        self.worker_bits = 5
        self.dc_bits = 5
        
        self.worker_shift = self.seq_bits
        self.dc_shift = self.seq_bits + self.worker_bits
        self.timestamp_shift = self.seq_bits + self.worker_bits + self.dc_bits
        self.sequence_mask = (1 << self.seq_bits) - 1

    def _curr_timestamp(self):
        return int(time.time() * 1000)

    def next_id(self):
        ts = self._curr_timestamp()
        
        if ts < self.last_timestamp:
            raise Exception("Clock moved backwards!")
            
        if ts == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.sequence_mask
            if self.sequence == 0:
                # Sequence exhausted, wait for next ms
                while ts <= self.last_timestamp:
                    ts = self._curr_timestamp()
        else:
            self.sequence = 0
            
        self.last_timestamp = ts
        
        # Construct ID
        new_id = ((ts << self.timestamp_shift) |
                  (self.datacenter_id << self.dc_shift) |
                  (self.worker_id << self.worker_shift) |
                  self.sequence)
        return new_id

def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (Snowflake) ---")
    gen1 = SnowflakeGenerator(worker_id=1, datacenter_id=1)
    gen2 = SnowflakeGenerator(worker_id=2, datacenter_id=1)
    
    id1 = gen1.next_id()
    id2 = gen2.next_id() # Different worker
    id3 = gen1.next_id() # Same worker, later time/seq
    
    print(f"✅ Valid ID (Sortable Int): {id1}")
    print(f"✅ Valid ID (Worker 2):     {id2}")
    print(f"✅ Valid ID (Next Seq):     {id3}")
    
    assert id1 < id3 # Time sortable!

if __name__ == "__main__":
    print("🧪 ID TEST: Auto-Inc (Bad) vs Snowflake (Good)\n")
    run_the_screwup()
    run_the_fix()
    
    print("\n🏆 Conclusion: Snowflake IDs are fast, unique, distributed-safe, and DB index friendly.")

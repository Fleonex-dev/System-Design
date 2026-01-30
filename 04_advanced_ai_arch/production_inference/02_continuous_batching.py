# 02_continuous_batching.py
import time
import queue
import random

# ==========================================
# 🌊 CONTINUOUS BATCHING (vLLM / Orca)
# ==========================================
# SCENARIO: 
# Req A (Long): "Write a book" (1000 tokens)
# Req B (Short): "Hi" (1 token)
#
# Static Batching: We wait for A to finish before returning B's slot. GPU wasted.
# Continuous Batching: As soon as B finishes, slot is freed for Req C.

class Request:
    def __init__(self, id, tokens_needed):
        self.id = id
        self.needed = tokens_needed
        self.generated = 0
        self.finished = False

class GPUEngine:
    def __init__(self, batch_size=4):
        self.batch_size = batch_size
        self.active_batch = []
        self.queue = queue.Queue()
        
    def add_request(self, req):
        self.queue.put(req)
        
    def step(self):
        # 1. Fill empty slots from queue
        while len(self.active_batch) < self.batch_size and not self.queue.empty():
            new_req = self.queue.get()
            self.active_batch.append(new_req)
            print(f"   🟢 [Engine] Allowed Req {new_req.id} into Batch")
            
        if not self.active_batch:
            return False
            
        # 2. Generate 1 token for everyone
        print(f"   ⚙️  [GPU] Running Batch: {[r.id for r in self.active_batch]}")
        
        finished_indices = []
        for i, req in enumerate(self.active_batch):
            req.generated += 1
            if req.generated >= req.needed:
                req.finished = True
                print(f"   🏁 [Engine] Req {req.id} Finished!")
                finished_indices.append(i)
                
        # 3. Evict finished (Continuous Batching!)
        # In Static Batching, we would wait for ALL to finish.
        for index in sorted(finished_indices, reverse=True):
            del self.active_batch[index]
            
        time.sleep(0.5)
        return True

def run_simulation():
    print("--- 🌊 Continuous Batching Demo ---")
    engine = GPUEngine(batch_size=2)
    
    # Mix of Long and Short requests
    engine.add_request(Request("Long-A", 10))
    engine.add_request(Request("Short-B", 2))
    engine.add_request(Request("Short-C", 2))
    
    step = 0
    while True:
        step += 1
        print(f"\n--- Step {step} ---")
        busy = engine.step()
        if not busy and engine.queue.empty():
            break
            
    print("\n🏆 Insight: Notice 'Short-C' entered while 'Long-A' was still running.")
    print("   This increases GPU utilization by 20-50%.")
    print("   🏢 Real World: Implemented in **vLLM** (Berkeley), **HuggingFace TGI**, and **Ray Serve**.")
    print("   Used by **AnyScale** and **Microsoft Azure** to maximize A100 efficiency.")

if __name__ == "__main__":
    run_simulation()

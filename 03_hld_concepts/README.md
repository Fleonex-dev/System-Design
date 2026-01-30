# ☁️ High Level Design (HLD)

> "Optimizing code is useless if your architecture bottlenecks network traffic."

This module covers **System Design** concepts required to scale from 1 user (Localhost) to 1,000,000 users (Distributed Cluster). We simulate these distributed concepts using Python threads/processes to show how they work internally.

## 🎓 Concepts Covered

### 1. Load Balancing (The Traffic Cop)
* **The Problem**: You have 3 GPU servers. Server A is processing a 10s prompt. Servers B and C are idle. A Round-Robin router sends the next request to A anyway. A crashes.
* **The Solution**: **Least-Connections** or **KV-Cache Aware** routing. Send traffic to the idle workers.

### 2. Caching (The Speed Boost)
* **The Problem**: 50% of your user queries are "Hello" or "Which model is this?". Generating these via GPT-4 takes 2s and costs $0.03.
* **The Solution**: **Semantic Caching**. Embed the query, check Vector DB. If similarity > 0.99, return cached answer. Time: 50ms. Cost: $0.

### 3. Consistent Hashing (The Sharding Key)
* **The Problem**: You store Vectors in 3 nodes. You add a 4th node. If using `hash(key) % N`, you have to move 100% of data. System goes down for days.
* **The Solution**: **Consistent Hashing Ring**. Only 1/N keys need moving.

### 4. Distributed IDs (Uniqueness at Scale)
* **The Problem**: Using `id++` (Auto Increment) in MySQL doesn't work when you have 5 DB masters.
* **The Solution**: **Snowflake IDs**. Time + MachineID + Sequence.

---

## 🧪 Experiments

| File | Concept | The "Screw Up" | The "Fix" |
|------|---------|----------------|-----------|
| `01_load_balancing.py` | Routing | Stuck in Queue (Round Robin) | Least-Connections Algorithm |
| `02_caching.py` | Caching | Expensive, slow API calls | Redis/Vector Cache Simulation |
| `03_hashing.py` | Sharding | Resharding 100% of keys | Consistent Ring (Resharding <30%) |
| `challenge.py` | Capstone | Dying API at 10k RPS | **Fix the Rate Limiter!** |

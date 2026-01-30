# ☁️ High Level Design (HLD)

> "Optimizing code is useless if your architecture bottlenecks network traffic."

This module covers **System Design** concepts required to scale from 1 user (Localhost) to 1,000,000 users (Distributed Cluster). We simulate these distributed concepts using Python threads/processes to show how they work internally.

## 🎓 Concepts Covered

### 1. Scaling 101 (Vertical vs Horizontal)
* **The Problem**: Your single server crashes when 100 users hit it.
*   **Vertical Scaling**: Buy a bigger machine ($$$). Limit: Physics.
*   **Horizontal Scaling**: Buy 10 cheap machines. Limit: Infinite.

### 2. Load Balancing (The Traffic Cop)
* **The Problem**: Server A is busy, B is idle. Round-Robin blindly sends to A.
* **The Solution**: **Least-Connections**. Send query to the node with fewest active requests.

### 3. Caching (KV & Semantic)
* **The Problem**: Generating tokens is slow (50ms/token).
* **The Solution**:
    *   **Semantic Cache**: Vector Similarity check.
    *   **KV Cache**: Store attention matrices.

### 4. Consistent Hashing (The Ring)
* **The Problem**: Adding a node to a hash map (`key % N`) reshuffles all keys.
* **The Solution**: **Virtual Nodes** on a Ring. Only K/N keys move.

### 5. Distributed IDs (Snowflake)
* **The Problem**: Auto-increment IDs fail in multi-master DBs.
* **The Solution**: **Snowflake ID**. Time + Machine + Sequence.

### 6. gRPC vs REST (Protobufs)
*   **The Problem**: JSON is slow (text parsing). HTTP/1.1 is serial.
*   **The Solution**: **gRPC**. Binary format (Protobuf), Multiplexing (HTTP/2), Strict Typing. 10x faster.

---

## 🧪 Experiments

| File | Concept | The "Screw Up" | The "Fix" |
|------|---------|----------------|-----------|
| `01_load_balancing.py` | Routing | Stuck in Queue (Round Robin) | Least-Connections Algorithm |
| `02_caching.py` | Caching | Expensive, slow API calls | Redis/Vector Cache Simulation |
| `03_hashing.py` | Sharding | Resharding 100% of keys | Consistent Ring (Resharding <30%) |
| `challenge.py` | Capstone | Dying API at 10k RPS | **Fix the Rate Limiter!** |

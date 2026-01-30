# 🏗️ System Design Patterns & Python Implementation

![Build Status](https://github.com/Fleonex-dev/System-Design/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)

> **"Show, Don't Just Tell."**
> A personal collection of verifiable, code-first System Design patterns.

Most System Design resources are static diagrams. This repository aims to make these concepts **executable** to understand how they actually work under the hood.
I built this to educate myself on **Race Conditions**, **Database Sharding**, **Consistent Hashing**, and **Distributed Transactions** by simulating them in Python.


---

## 🚀 What's Inside?

### 1. Python Essentials for Scale
*   **Concurrency**: Threads vs Processes, AsyncIO Event Loops, and GIL limitations.
*   **Thread Safety**: Locks, Semaphores, and Deadlock simulations (Dining Philosophers).

### 2. High Level Design (HLD) & Resiliency
*   **Scalability**: Vertical vs Horizontal Scaling, Load Balancing algorithms.
*   **Distributed Data**: CAP Theorem, Replication Lag, Sharding (Range vs Hash), and **Saga Pattern**.
*   **Resiliency**: Circuit Breakers (Netflix Hystrix), Retry with Jitter, and **Chaos Engineering**.
*   **Advanced Structures**: Bloom Filters, HyperLogLog, and **Geospatial QuadTrees** (Uber).

### 3. Advanced AI Architecture (SOTA)
*   **Production Inference**: **vLLM** (Continuous Batching), **KV Caching** (PagedAttention), and **LoRA** Adapters.
*   **Recommender Systems**: **Two-Tower Architecture** (YouTube/Netflix style).
*   **RAG Deep Dive**: Vector Indexing (HNSW), Chunking strategies, and Embeddings.

### 4. ⚔️ Interview Prep & Experiments
A set of common interview questions implemented with both "Naive" (Bad) and "Optimal" (Scaled) approaches to demonstrate the difference.

| Component | The "Naive" Way (Fail) | The "Optimal" Way (Pass) |
| :--- | :--- | :--- |
| **Q4. WhatsApp** | Polling DB every 1s | WebSockets + Store-and-Forward |
| **Q6. News Feed** | Pull Model (Slow Read) | Push Model (Fan-out on Write) |
| **Q7. Google Drive** | Re-uploading 1GB Files | Block-level Deduplication |
| **Q8. YouTube** | Sending full 4K.mp4 | Adaptive Bitrate (HLS/DASH) |
| **Q9. Leaderboard** | `ORDER BY score` | Redis Sorted Sets (SkipList) |
| **Q10. Ticketmaster** | Race Condition (Oversell) | Optimistic Locking / Lua Scripts |
| **Q11. Analytics** | INSERT every click | Stream Windows (Flink/Spark) |
| **Q12. Trending** | HashMap (OOM) | Count-Min Sketch (Probabilistic) |
| **Q13. Kafka** | In-Memory Queue | Distributed Append-Only Log |
| **Q15. Payments** | Retrying on Timeout | Idempotency Keys |

---

## 🏢 Real World Architecture References
I included references to where these patterns are used in production systems:
*   **Uber/Google Maps**: QuadTrees & Geohashing.
*   **Netflix**: Chaos Monkey & Hystrix.
*   **Discord**: Consistent Hashing (Ring).
*   **Amazon**: Saga Pattern for Order Fulfillment.
*   **Apple Intelligence**: LoRA Adapters for On-Device AI.
*   **YouTube**: Two-Tower Neural Networks for Recommendations.

---

## 🛠️ How to Run

1.  **Setup**:
    ```bash
    make setup
    ```

2.  **Start Learning**:
    ```bash
    make run
    ```
    *(Navigate the CLI menu to choose lessons)*


3.  **Run Tests**:
    ```bash
    make test
    ```
4.  **Clean**:
    ```bash
    make clean
    ```

---

## 🤝 Contributing
Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on the workflow.
1.  Fork the repo
2.  Create your feature branch (`git checkout -b feat/amazing-feature`)
3.  Run tests (`make test`)
4.  Commit your changes (`git commit -m 'feat: Add amazing feature'`)
5.  Push to the branch (`git push origin feat/amazing-feature`)
6.  Open a Pull Request

---

*Created for self-education and shared for the community*
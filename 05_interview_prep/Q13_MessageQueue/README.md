# 📨 System Design: Message Queue (Kafka)

## 🧠 The Concept
Decoupling producers (Loggers) from consumers (Analytics). High throughput, durable storage.

## 🛑 The Challenge (Naive Approach)
*   **Method**: In-Memory Queue (`collections.deque` or `list`).
*   **Problem**:
    1.  **Data Loss**: If server crashes, RAM is wiped. All messages lost.
    2.  **Backpressure**: If consumer is slow, producer fills up RAM -> OOM.

## ✅ The Solution (Optimal)
*   **Strategy**: **Distributed Commit Log** (Kafka).
*   **Storage**: Append-Only File on Disk (Sequential writes are fast).
*   **Scalability**:
    *   **Partitions**: Split topic into Shards.
    *   **Consumer Groups**: Parallel reading.

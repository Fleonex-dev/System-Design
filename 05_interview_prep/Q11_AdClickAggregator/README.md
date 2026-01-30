# 📉 System Design: Ad Click Aggregator / Analytics

## 🧠 The Concept
Counting clicks/views in real-time for billing. High volume (1M+ events/sec).

## 🛑 The Challenge (Naive Approach)
*   **Method**: `UPDATE ad_counts SET clicks = clicks + 1 WHERE ad_id = X`.
*   **Problem**:
    1.  **DB Lock Contention**: 1000 threads trying to update the same row.
    2.  **Latency**: Writes are slow.

## ✅ The Solution (Optimal)
*   **Strategy**: **Stream Processing** (MapReduce).
*   **Architecture**:
    1.  **Ingest**: Kafka stores raw events.
    2.  **Process**: Flink/Spark Streaming aggregates events in **Time Windows** (e.g. 1 minute).
    3.  **Store**: Write the *aggregated* count (+1000) to DB once per minute.

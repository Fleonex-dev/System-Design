# 📊 System Design: Metrics & Monitoring (Datadog)

## 🧠 The Concept
Ingesting millions of data points (CPU, RAM) per second. **Write-Heavy** system.

## 🛑 The Challenge (Naive Approach)
*   **Method**: Writing every metric directly to SQL.
*   **Problem**:
    1.  **I/O Bottleneck**: Disk cannot handle random writes at that scale.
    2.  **Locking**: Database locks up.

## ✅ The Solution (Optimal)
*   **Strategy**: **Buffering & Batching**.
    *   buffer metrics in memory for 10s.
    *   flush in bulk to storage.
*   **Protocol**: **UDP** (Fire and forget) is often used over TCP to reduce overhead.
*   **Storage**: **Time-Series DB** (InfluxDB/Prometheus) optimized for append-only writes.

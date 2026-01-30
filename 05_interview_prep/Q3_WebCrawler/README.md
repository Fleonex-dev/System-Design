# 🕷️ System Design: Distributed Web Crawler

## 🧠 The Concept
Indexing the internet (Google/Bing). Visiting billions of pages efficiently.

## 🛑 The Challenge (Naive Approach)
*   **Method**: Recursive DFS (Depth First Search) in a `while` loop.
*   **Problem**:
    1.  **Cycles**: A links to B, B links to A -> Infinite Loop.
    2.  **Politeness**: Spamming a server with 1000 requests/sec.
    3.  **Memory**: `visited` set grows too large for RAM.

## ✅ The Solution (Optimal)
*   **Architecture**:
    *   **Frontier Queue**: Kafka/SQS to manage URLs to visit.
    *   **Deduplication**: **Bloom Filter** (Probabilistic structure) to verify "Have I seen this URL?" with minimal RAM.
    *   **Politeness**: Per-domain queues with delays.

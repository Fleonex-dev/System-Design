# 🔍 System Design: Distributed Search (Elasticsearch)

## 🧠 The Concept
Searching billions of documents (e.g. Logs, E-commerce products) by keyword in milliseconds.

## 🛑 The Challenge (Naive Approach)
*   **Method**: `grep` or SQL `LIKE '%keyword%'`.
*   **Problem**:
    1.  **Full Table Scan**: O(N). Scans every single character of every document. Extremely slow.

## ✅ The Solution (Optimal)
*   **Data Structure**: **Inverted Index**.
    *   Map `Term -> [DocID, DocID, ...]`.
    *   "Burger" -> [1, 5, 8].
    *   Lookups are O(1) or O(log N).
*   **Distribution**:
    *   **Sharding**: Split index by Document ID.
    *   **Scatter-Gather**: Send query to all shards, merge results (TF-IDF ranking).

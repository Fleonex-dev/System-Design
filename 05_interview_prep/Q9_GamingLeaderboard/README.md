# 🏆 System Design: Live Gaming Leaderboard

## 🧠 The Concept
Real-time ranking of millions of players (e.g. Fortnite, MMORPGs).

## 🛑 The Challenge (Naive Approach)
*   **Method**: SQL Database `ORDER BY`.
    *   `SELECT * FROM scores ORDER BY value DESC LIMIT 10`
*   **Problem**:
    1.  **Sorting Cost**: Sorting 10 million rows on every update is O(N log N). Too slow for real-time.

## ✅ The Solution (Optimal)
*   **Technology**: **Redis Sorted Sets (ZSET)**.
*   **Data Structure**: **Skip List** (O(log N)).
*   **Operations**:
    *   `ZADD player_score 100 "Alice"` -> Inserts in correct position instantly.
    *   `ZREVRANGE 0 10` -> Gets top 10 instantly.

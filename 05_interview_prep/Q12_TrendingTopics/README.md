# 🔥 System Design: Trending Topics (Twitter Trends)

## 🧠 The Concept
Finding the "Top K" most frequent items in a stream of billions of items.

## 🛑 The Challenge (Naive Approach)
*   **Method**: Python Dictionary `word -> count`.
*   **Problem**: **OOM (Out of Memory)**.
    *   There are billions of unique words/hashtags. Storing all of them requires Terabytes of RAM.

## ✅ The Solution (Optimal)
*   **Data Structure**: **Count-Min Sketch** (CMS).
    *   A probabilistic 2D array (Matrix) of counters.
    *   Uses hash functions to map words to indices.
    *   **Space**: Fixed size (e.g., 2MB) regardless of input size.
    *   **Trade-off**: Small error margin (overcounting), but never crashes.

# 🚦 System Design: Distributed Rate Limiter

## 🧠 The Concept
Preventing a single user or IP from overwhelming your API. Used by Stripe, Twitter,/X, and Cloudflare.

## 🛑 The Challenge (Naive Approach)
*   **Method**: Storing `IP -> Count` in a Python Dictionary.
*   **Problem**:
    1.  **Race Conditions**: Two requests read "9", both increment to "10", both pass.
    2.  **Memory Leak**: Keys are never expired.
    3.  **Local Only**: Doesn't work if you have 2+ servers.

## ✅ The Solution (Optimal)
*   **Algorithm**: **Token Bucket** or **Sliding Window Log**.
*   **Storage**: **Redis** (In-Memory Key-Value Store).
*   **Logic**:
    *   Use `INCR` or `Lua Scripts` for atomicity.
    *   Use `TTL` (Time To Live) to auto-expire keys.

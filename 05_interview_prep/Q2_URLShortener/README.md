# 🔗 System Design: URL Shortener (TinyURL)

## 🧠 The Concept
Compresse long URLs into short, shareable links (e.g. `bit.ly/3xZy`).

## 🛑 The Challenge (Naive Approach)
*   **Method**: `random.choice()` string generation.
*   **Problem**:
    1.  **Collisions**: Randomly generating "abc" twice requires checking the DB (slow).
    2.  **Unpredictable**: Length grows arbitrarily.

## ✅ The Solution (Optimal)
*   **Algorithm**: **Base62 Encoding**.
    *   Map a unique Integer ID (1001) -> Base62 ("g7").
*   **ID Generation**:
    *   **Ticket Server** (Flicker) or **Snowflake ID** (Twitter) to generate unique integers across distributed servers.
    *   No collisions by design.

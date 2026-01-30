# 📰 System Design: News Feed (Facebook/Twitter)

## 🧠 The Concept
Showing a personalized timeline of posts from friends.

## 🛑 The Challenge (Pull Model)
*   **Method**: Query on Read.
    *   `SELECT * FROM posts WHERE user_id IN (my_friends) ORDER BY date`
*   **Problem**:
    *   **Slow Reads**: If you follow 1000 people, DB has to scan millions of rows every time you open the app.

## ✅ The Solution (Push Model / Fan-out)
*   **Strategy**: **Fan-out on Write**.
    *   When Justin Bieber posts, we asynchronously "push" that post ID into the pre-computed feed of all 100M followers.
*   **Read**: `GET /feed` is O(1) - just reading a pre-built list from Redis.

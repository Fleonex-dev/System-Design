# 💬 System Design: Real-time Chat (WhatsApp/Slack)

## 🧠 The Concept
Delivering messages instantly between millions of users while handling offline states.

## 🛑 The Challenge (Naive Approach)
*   **Method**: Polling the database.
*   **Problem**:
    1.  **Latency**: Delay between polling intervals.
    2.  **Server Load**: 1 Billion users polling every second = Database Explosion.

## ✅ The Solution (Optimal)
*   **Protocol**: **WebSockets** (Persistent Duplex Connection).
*   **Architecture**:
    *   **Stateful Gateway**: Maintains connection map (`UserA -> SocketID`).
    *   **Pub/Sub**: Redis PubSub to route messages between different gateway servers.
    *   **Store-and-Forward**: If UserB is offline, store in Cassandra/HBase and deliver when online.

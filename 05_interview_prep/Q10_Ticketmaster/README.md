# 🎫 System Design: Ticketmaster / Booking System

## 🧠 The Concept
Selling a limited resource (seats) to millions of concurrent users.

## 🛑 The Challenge (Naive Approach)
*   **Method**: Read-then-Write (Check if seat is free, then book it).
*   **Problem**: **Race Condition**. 
    *   User A and User B check Seat 1A at the same ms. Both see "Free". Both book.
    *   Result: Double Booking (Oversell).

## ✅ The Solution (Optimal)
*   **Strategy**: **Distributed Locking** or **Optimistic Concurrency Control**.
    *   **Postgres**: `SELECT ... FOR UPDATE` (Pessimistic Lock).
    *   **Redis**: `SET resource_id user_id NX PX 10000` (Distributed Lock).
    *   **Lua Script**: Check and Set in one atomic step.

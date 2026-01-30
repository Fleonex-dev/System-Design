# ☁️ High Level Design (HLD): Distributed Systems Internals

> **Target Audience**: Architects designing systems for 1M+ RPS.
> **Scope**: Consensus, Partitioning Strategies, and Failure Modes.

---

## 1. The CAP Theorem (Reality Check)
You can only have 2 of 3: **Consistency**, **Availability**, **Partition Tolerance**.
*   **Partition Tolerance (P)** is non-negotiable in distributed systems (networks fail).
*   **The Choice**:
    *   **CP (Consistency > Availability)**: MongoDB / Hbase / Redis (single leader). If the Leader dies or splits, the system rejects writes until a new leader is elected (Downtime).
    *   **AP (Availability > Consistency)**: Cassandra / DynamoDB. Nodes accept writes even if disconnected. Result: **Eventual Consistency** (Conflict Resolution required later).

---

## 2. Consistent Hashing (The Ring)

### The Problem: Modulo Hashing
`server_index = hash(key) % N`.
*   If `N` changes (Server crash/add), nearly **100% of keys** map to a new index.
*   **Result**: Massive Cache Stampede. The DB melts down.

### The Solution: The Ring
*   **Mechanism**: Map both Servers and Keys to a 360-degree circle (0 to $2^{32}$).
*   **Routing**: Key $K$ is stored on the first Server found moving clockwise.
*   **Scaling**: Adding a server only "steals" keys from its immediate neighbor.
*   **Virtual Nodes**: To prevent "Hotspots" (one server getting a popular segment), each physical server maps to 100+ random points on the ring.

---

## 3. Distributed Transactions (Saga Pattern)

### The ACID Problem
You cannot easily do `BEGIN TRANSACTION` across Microservice A (Orders) and Microservice B (Payment).
Two-Phase Commit (2PC) is blocking and slow (`O(N^2)` messages).

### The Saga Solution
*   **Mechanism**: A sequence of local transactions.
*   **Rollback**: If Step 3 fails, execute **Compensating Transactions** for Step 2 and Step 1 in reverse order.
    *   *Step 1*: Reserve Flight (Success).
    *   *Step 2*: Reserve Hotel (Success).
    *   *Step 3*: Charge Card (Fail).
    *   *Compensate 2*: Cancel Hotel.
    *   *Compensate 1*: Cancel Flight.

---

## 4. Caching Internal

### Write Strategies
1.  **Write-Through**: Write to Cache + DB synchronously. Safe, slow writes.
2.  **Write-Back (Write-Behind)**: Write to Cache, ack immediately. Flush to DB async. Fast, risk of data loss on crash.
3.  **Cache-Aside**: App reads DB, populates Cache. App writes DB, invalidates Cache. Most common.

### Eviction Policies
*   **LRU (Least Recently Used)**: LinkedHashMap. Good general purpose.
*   **LFU (Least Frequently Used)**: Better for "long tail" patterns (e.g. Homepage content).
*   **TinyLFU**: Uses Bloom Filters to approximate frequency with minimal memory (used in Caffeine/Ristretto).

---

## 🧪 Simulation Files
*   `03_consistent_hashing.py`: Implementation of the Ring and Virtual Nodes.
*   `distributed_data/05_saga_pattern.py`: Implementing Compensating Transactions.
*   `01_llm_load_balancing.py`: Least-Connection routing simulation.

# 🐍 Python Essentials for System Design

> "Premature optimization is the root of all evil, but standard Python is slow by default."

This module covers the **foundational Python concepts** that separate a "scripting" developer from a "systems" engineer. In the context of LLM Agents and High-Load systems, understanding these is non-negotiable.

## 🎓 Concepts Covered

### 1. Concurrency (VS Parallelism)
* **The Problem**: Python has a GIL (Global Interpreter Lock). Only one thread runs Python bytecode at a time.
* **The Implication**: Multithreading is useless for CPU-bound tasks (math, data processing) but great for I/O-bound tasks (network requests, DB queries).
* **The Solution**:
    * **Asyncio**: Cooperative multitasking. Single-threaded, but zero context-switching overhead. **Crucial for LLM serving** where you wait for tokens 99% of the time.
    * **Multiprocessing**: Spawns totally new processes (new PIDs) to bypass GIL. Heavy memory usage but true parallelism.

### 2. Typing & Pydantic
* **The Problem**: Big dictionaries (`{...}`) are convenient but dangerous. One typo in a key name crashes production 3 months later.
* **The Solution**: **Pydantic**. It forces structure, validates data at the door (ingress), and gives you autocomplete in IDEs.

### 3. Generators (`yield`)
* **The Problem**: Loading a 100GB CSV into a list crashes RAM.
* **The Solution**: Process one row at a time. Essential for **Streaming Responses**.

### 4. Context Managers (`with`)
*   **The Problem**: Forgetting to close a file or release a Lock causes leaks/deadlocks.
*   **The Solution**: `__enter__` and `__exit__`. Auto-cleanup resources (like DB connections).

### 5. Decorators (`@wrapper`)
*   **The Problem**: Copy-pasting "Logging" or "Timing" code into 50 functions.
*   **The Solution**: Higher-Order Functions. Wrap logic (like `@retry`, `@lru_cache`) transparently.

---

## 🧪 Experiments

| File | Concept | The "Screw Up" | The "Fix" |
|------|---------|----------------|-----------|
| `01_concurrency.py` | Asyncio | Blocking the event loop with `requests.get` | Using `aiohttp` for 100x concurrency |
| `02_typing.py` | Pydantic | `KeyError` at runtime | Robust implementation with validation |
| `challenge.py` | Capstone | A broken, slow API script | **You fix it!** |

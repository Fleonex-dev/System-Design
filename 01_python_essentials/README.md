# 🐍 Python Internals & Performance Patterns

> **Target Audience**: Staff+ Engineers optimizing high-throughput systems.
> **Scope**: Memory models, GIL mechanics, Event Loops, and Runtime Validation.

---

## 1. The Global Interpreter Lock (GIL) & Concurrency model

### The Internals
CPython's memory management is not thread-safe. To prevent race conditions on reference counts (`PyObject_HEAD`), a global mutex (the GIL) enforces that **only one thread executes Python bytecode at a time**.

### Implications for Scale
1.  **CPU-Bound Tasks** (JSON parsing, Crypto, Matrix Math):
    *   Adding threads **degrades performance** due to context-switching overhead and lock contention.
    *   *Solution*: `multiprocessing` (spawns new JVM/Interpreter instances, separate memory space) or C-extensions (numpy releases GIL).
2.  **I/O-Bound Tasks** (HTTP, DB Queries):
    *   The GIL is **released** when the thread waits for I/O (syscalls).
    *   *Solution*: `threading` works, but `asyncio` is superior for high connection counts (C10K problem).

### Why AsyncIO? (The Event Loop)
*   **Mechanism**: Uses `epoll` (Linux) or `kqueue` (MacOS) to monitor file descriptors (sockets) for readability/writability.
*   **Cost**: Single-threaded. Zero OS context switching. Extremely low memory footprint per "task" compared to OS threads (which reserve ~8MB stack).
*   **The Trap**: Any blocking call (`time.sleep`, `requests.get`) inside an `async def` halts the **entire** loop. Watchdog timers are required in production.

---

## 2. Memory Management: Generators vs Iterators

### Eager Evaluation (Bad)
```python
def get_logs():
    return [line for line in open("10gb.log")] # 💥 OOM Kill
```
*   **Behavior**: Allocates memory for ALL elements immediately.
*   **Cost**: O(N) Memory.

### Lazy Evaluation (Good)
```python
def get_logs():
    for line in open("10gb.log"):
        yield line # 🧠 Pauses stack frame
```
*   **Behavior**: `yield` suspends the function's execution, saving local variables and instruction pointer.
*   **Cost**: O(1) Memory. The data exists only as it passes through the CPU cache.
*   **Use Case**: Streaming LLM tokens, ETL pipelines, infinite streams.

---

## 3. Metaprogramming: Decorators & Closures

### The Mechanics
A decorator is a Higher-Order function that returns a **Closure**.
```python
def retry(func):
    def wrapper(*args, **kwargs): # Closure capturing 'func'
        try:
            return func(*args, **kwargs)
        except:
            return func(*args, **kwargs)
    return wrapper
```

### Performance Impact
*   **Call Overhead**: Every decorated function adds a standard Python function call overhead (~100ns).
*   **Stack Depth**: Deeply nested decorators can hit recursion limits or make stack traces unreadable.
*   **Best Practice**: Always use `@functools.wraps(func)` to copy metadata (`__name__`, `__doc__`). Without this, monitoring tools (DataDog/NewRelic) cannot identify your functions.

---

## 4. Robustness: Context Managers (`with`)

### The Protocol
Relies on `__enter__` (setup) and `__exit__` (teardown).
Crucially, `__exit__` is **guaranteed** to run even if an exception occurs in the block.

### Anti-Pattern: Reliance on GC
```python
f = open("file.txt")
f.read()
# Relying on Garbage Collector to close 'f' when it goes out of scope.
```
*   **Risk**: In CPython, ref-counting usually closes it immediately. In PyPy or generally loaded systems, GC is non-deterministic. Failure to close leads to **"Too many open files" (EMFILE)** errors.
*   **Fix**: Always use `with open(...)`.

---

## 5. Runtime Validation: Pydantic vs `typing`

### Static vs Runtime
*   **`typing.List[int]`**: Erasure. Ignored at runtime. Zero cost, but zero safety against `json.load()` returning strings.
*   **`Pydantic`**: Runtime parsing and validation.

### Performance (V2)
Pydantic V2 is rewritten in **Rust**.
*   **Ingress**: Use Pydantic at the "Edge" (API Endpoints, Kafka Consumers) to guarantee strict types entering your domain.
*   **Internals**: Once validated, pass raw objects/dataclasses internally to avoid validation overhead in hot loops.

---

## 🧪 Simulation Files
*   `concurrency/`: Race conditions, Deadlocks, and AsyncIO event loops.
*   `02_typing.py`: Benchmarking Dict access vs Pydantic validation cost.
*   `03_generators.py`: Memory profiling Generator vs List.

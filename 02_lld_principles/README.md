# 🧩 Low Level Design (LLD): The Architecture of Agents

> **Target Audience**: Engineers building maintainable AI Systems, not just scripts.
> **Scope**: Dependency Injection, Protocol-based Interfaces, and Composition.

---

## 1. The SOLID Principles (Agent Specific)

### Single Responsibility (SRP)
*   **The Smell**: A `ChatBot` class that handles Prompt Engineering, OpenAI API calls, AND saving to Postgres.
*   **The Fix**: Decouple `PromptBuilder`, `LLMClient`, and `ChatRepository`. Use Dependency Injection so the `ChatBot` logic is purely orchestration.

### Open/Closed (OCP)
*   **The Smell**: Adding a new "Tool" (e.g. Google Search) requires modifying the main `Agent.run()` method with `if tool == 'google': ...`.
*   **The Fix**: Create an abstract `Tool` interface. The Agent iterates over `List[Tool]`. New tools are just new classes complying with the interface.

### Dependency Inversion (DIP)
*   **The Smell**: `import openai` at the top of your domain logic.
*   **The Fix**: Depend on abstractions. Define a `ModelProvider` protocol.
    *   *Benefit*: Swap OpenAI for `LocalLLaMA` or `Claude` during unit tests or production outages without changing a single line of business logic.

---

## 2. Interface Contracts in Python: `abc` vs `Protocol`

### Abstract Base Classes (`abc`)
*   **Mechanism**: Nominal Typing. `class OpenAI(LLMProvider): ...`
*   **pros**: Runtime enforcement. You can't instantiate it if methods are missing.
*   **Cons**: Rigid hierarchy.

### Protocols (Structural Typing / Duck Typing)
*   **Mechanism**: Static Analysis (`mypy`). "If it walks like a duck..."
*   **Benefit**: You can make 3rd party libraries (like `langchain` objects) comply with *your* interfaces without inheritance. This is Python's answer to Go Interfaces.

---

## 3. Composition over Inheritance

### The Inheritance Trap
*   **Scenario**: `BaseAgent` -> `ConversationalAgent` -> `MemoryAgent` -> `RAGMemoryAgent`.
*   **Problem**: What if you want a `RAGAgent` without "Memory"? You can't. You get the Gorilla with the Banana.

### The Composition Fix
*   **Mechanism**: `Agent` *has-a* `MemoryModule`. `Agent` *has-a* `RetrievalModule`.
*   **Injection**: Pass these modules into `__init__`.
    ```python
    agent = Agent(
        memory=RedisMemory(),
        retrieval=ChromaDBRetriever()
    )
    ```

---

## 4. Design Patterns for AI

### Factory Pattern
*   **Use Case**: Dynamically loading models based on reliability/cost.
*   **Implementation**: `ModelFactory.get_model("gpt-4" if expensive else "mistral")`.

### Observer Pattern
*   **Use Case**: Streaming Tokens to multiple outputs (Console, WebUI, Logger).
*   **Implementation**: The generation loop `notify()`s subscribers on ever token.

### Strategy Pattern
*   **Use Case**: Swapping RAG strategies.
    *   *Strategy A*: Keyword Search (Fast).
    *   *Strategy B*: HyDE + Vector Search (Slow, Accurate).
    *   *Runtime*: Pick strategy based on query complexity.

---

## 🧪 Simulation Files
*   `01_solid_agents.py`: Refactoring a Monolith into SOLID components.
*   `design_patterns/`: Implementations of Factory, Observer, and Strategy.

# 🧩 Low Level Design (LLD) for AI Engineers

> "Bad architecture is like a loan: giving you speed now but slowing you down forever with interest."

Writing a script to call OpenAI is easy. Building a system that supports OpenAI, Anthropic, Local LLaMA, streaming, and tool use *without* rewriting everything is hard. That's where LLD comes in.

## 🎓 Concepts Covered

### 1. SOLID Principles (The Agent Edition)
* **S**ingle Responsibility: An Agent shouldn't also be a Database.
* **O**pen/Closed: Add new Tools without changing the Agent code.
* **L**iskov Substitution: A `LocalLLM` class should work exactly like `OpenAI` class.
* **I**nterface Segregation: Don't force a simple Chatbot to implement `generate_image()`.
* **D**ependency Inversion: Your Agent should depend on an abstract `LLMProvider`, not `import openai`.

### 2. Design Patterns
* **Factory**: Stop writing `if model == 'gpt4': ...`. Use a Factory to sprout objects.
* **Observer**: Don't poll for updates. Let the system notify you. (Crucial for async agent workflows).
* **Strategy**: Swap algorithms at runtime (e.g., changing from "Vector Search" to "Keyword Search" on the fly).
* **Adapter**: Make incompatible interfaces work together (e.g., fitting a new Vector DB into your existing pipeline).

---

## 🧪 Experiments

| File | Pattern | The "Screw Up" | The "Fix" |
|------|---------|----------------|-----------|
| `01_solid_agents.py` | SOLID | A God-class Bot that does everything | Clean Interfaces (SRP/DIP) |
| `02_factory.py` | Factory | Conditional Spaghetti `if/else` | extensible `get_llm()` |
| `03_strategy.py` | Strategy | Hardcoded RAG Logic | Swappable Retrieval Strategies |
| `04_observer.py` | Observer | resource-heavy Polling | Event-Driven Updates |
| `challenge.py` | Capstone | A Monolithic Chatbot | **Refactor it!** |

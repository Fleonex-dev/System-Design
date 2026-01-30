# 🧠 Advanced AI Architectures

> "Any sufficiently advanced technology is indistinguishable from magic." - Arthur C. Clarke (and potentially GPT-5)

This module moves beyond basic chatbots into the **cutting-edge architectures** used by labs like OpenAI, Anthropic, and Google DeepMind. We are talking about techniques to make models smarter (Reasoning), faster (Speculative Decoding), and more efficient (MoE).

## 🎓 Concepts Covered

### 1. RAG Optimization (Beyond Vector Search)
* **The Problem**: A user asks "What is the capital of the moon?". Vector search finds a random sci-fi book. The LLM hallucinates "Luna City".
* **The Solution**: **HyDE** (Hypothetical Document Embeddings) generating a fake answer to search for, and **Re-ranking** (Cross-Encoders) to verify relevance.

### 2. Agent Orchestration (Reliable Autonomy)
* **The Problem**: You give an agent a loop. It gets stuck saying "Thinking..." forever.
* **The Solution**: **Directed Acyclic Graphs (DAGs)**. Represent state as a graph. Force progress. This is the logic behind Libraries like LangGraph.

### 3. Inference Optimization (Speed)
* **The Problem**: Generating 100 tokens takes 5 seconds (50ms/token).
* **The Solution**: **Speculative Decoding**. A tiny model guesses 5 words ("The cat sat on the..."). The big model verifies them in batch. 2-3x speedup.

### 4. Mixture of Experts (MoE)
* **The Problem**: A 70B parameter model is too expensive to run for every query.
* **The Solution**: **MoE**. Have 8 "Experts" (Math expert, Code expert, etc.). Only activate 2 for each token. "Sparse" activation means vast knowledge but cheap inference.

### 5. Reasoning (System 2 Thinking)
* **The Problem**: LLMs are "System 1" (Fast, Intuitive). They suck at complex math/logic puzzles because they just predict the next word.
* **The Solution**: **Tree of Thoughts / MCTS**. Generate multiple thoughts, evaluate them, explore the best path. This is how AlphaGo won, and arguably how "o1" works.

---

## 🧪 Experiments

| File | Concept | The "Screw Up" | The "Fix" |
|------|---------|----------------|-----------|
| `01_rag_opt.py` | RAG | Naive Cosine Similarity failures | HyDE + Re-ranking simulation |
| `02_agents.py` | Orchestration | Infinite Loops (ReAct) | Finite State Machine / DAG |
| `03_inference.py` | Speed | Serial Decoding (Slow) | Speculative Decoding verification |
| `04_moe.py` | Architecture | Dense Activation (Heavy) | Sparse Gating (Efficient) |
| `05_reasoning.py` | Intelligence | Zero-shot Hallucination | Tree of Thoughts Search |
| `challenge.py` | Capstone | Basic Bot | **Build an AGI Prototype** |

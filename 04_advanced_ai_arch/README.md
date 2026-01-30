# 🧠 Advanced AI Architectures: Engineering & Math

> **Target Audience**: ML Engineers shipping SOTA models to production.
> **Scope**: Attention Memory Math, KV Cache Paging, and Speculative execution.

---

## 1. LLM Serving Math (Where does the RAM go?)

### Model Weights
*   Simple rule: `Params * Precision`.
*   **70B Model (FP16)**: $70 \times 10^9 \times 2 \text{ bytes} \approx 140 \text{ GB}$ VRAM.
*   **Quantization (INT4)**: $70 \times 10^9 \times 0.5 \text{ bytes} \approx 35 \text{ GB}$ VRAM. (Feasible on 2x A100 or 1x A6000 Ada).

### The KV Cache (The Bottleneck)
During decoding, the model must "attend" to all previous tokens. Re-computing keys/values is O($N^2$).
Instead, we cache them.
*   **Size**: $2 \times \text{Layers} \times \text{Heads} \times \text{Dim} \times \text{Precision} \times \text{ContextLength}$.
*   **Impact**: For long context (128k), the KV Cache can exceed the Model Weights in size.
*   **vLLM Solution**: **PagedAttention**. Allocating KV blocks in non-contiguous memory (like OS Virtual RAM) to prevent fragmentation and OOM.

---

## 2. Retrieval Augmented Generation (RAG) at Scale

### The Naive Pipeline
`Query -> Similarity Search -> Top 3 Chunks -> Context`.
*   **Failure Mode**: "Semantic drift". The query "moon capital" matches sci-fi text better than astronomy text.

### Advanced RAG Techniques
1.  **HyDE (Hypothetical Document Embeddings)**:
    *   Ask LLM to *hallucinate* a fake answer.
    *   Embed the *answer*.
    *   Search for documents matching the hallucination. (Matches style/domain better than the query).
2.  **Cross-Encoders (Re-ranking)**:
    *   Bi-Encoder (Vector DB) is fast ($O(1)$) but imprecise (cosine sim).
    *   Cross-Encoder is slow ($O(N)$) but precise (takes pairs of `(Query, Doc)` and scores them 0-1).
    *   *Production Path*: Vector Search (Retrieve 100) -> Cross-Encoder (Re-rank to Top 5).

---

## 3. Speculative Decoding

### The Latency Problem
LLMs are memory-bandwidth bound. Moving 140GB of weights to compute 1 token takes time (e.g. 50ms).
GPU Compute cores sit idle waiting for memory.

### The Algorithm
1.  **Draft**: A tiny model (7B) generates 5 low-quality tokens quickly (10ms).
2.  **Verify**: The big model (70B) runs *once* in parallel on those 5 tokens.
3.  **Accept/Reject**: If draft matches big model's probability distribution, keep them.
*   **Result**: 2-3x speedup with mathematically identical output to the big model.

---

## 4. Mixture of Experts (MoE)

### Sparse Activation
*   **Mixtral 8x7B**: Has 47B parameters, but only uses 13B per token.
*   **Routing**: A "Router" network predicts which 2 experts (out of 8) are best for the current token.
*   **Memory vs Compute**: High Memory usage (must load all weights), Low Compute (only multiply small subset). Ideal for high throughput serving if VRAM is abundant.

---

## 🧪 Simulation Files
*   `production_inference/01_kv_cache.py`: Implementing a KV Cache from scratch to see memory growth.
*   `optimization/03_inference_optimization.py`: Simulating Speculative Decoding acceptance rates.
*   `04_moe.py`: A routing simulation for sparse experts.

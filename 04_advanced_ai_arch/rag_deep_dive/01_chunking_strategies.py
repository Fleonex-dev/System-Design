# 01_chunking.py

# ==========================================
# ✂️ RAG CHUNKING STRATEGIES
# ==========================================
# SCENARIO: You have a large PDF. You need to split it for retrieval.
# The split method MATTERS.

text = """
The Apollo 11 mission launched on July 16, 1969.
Neil Armstrong was the commander.
Buzz Aldrin was the pilot.
They landed on the moon.
"""

# 1. FIXED SIZE (Naive)
def fixed_chunking(text, size=30):
    print("--- 🛑 Fixed Size Chunking ---")
    chunks = [text[i:i+size] for i in range(0, len(text), size)]
    for i, c in enumerate(chunks):
        # Problem: Splits sentences in half! "Neil Arms" | "trong was..."
        print(f"[{i}] '{c.replace(chr(10), ' ')}'")

# 2. RECURSIVE / SEMANTIC (Smart)
def semantic_chunking(text):
    print("\n--- ✅ Semantic Chunking ---")
    # In prod, usage of LangChain RecursiveCharacterTextSplitter
    # or NLTK sentence tokenizer.
    # Here, we split by Logical Delimiters (Newlines/Sentences).
    
    sentences = text.strip().split('\n')
    for i, s in enumerate(sentences):
        print(f"[{i}] '{s}'") # Keeps meaning intact!

if __name__ == "__main__":
    fixed_chunking(text)
    semantic_chunking(text)
    print("\n🏆 Conclusion: Bad chunking = Bad retrieval. Context is lost.")

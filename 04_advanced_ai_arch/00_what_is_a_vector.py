# 00_what_is_a_vector.py
import math

# ==========================================
# 🏹 WHAT IS A VECTOR? (Embeddings)
# ==========================================
# Computers don't understand text. They understand numbers.
# An "Embedding" turns text into a list of numbers (a Vector).
#
# Similar words have similar directions.
# "King" -> [0.9, 0.1]
# "Queen" -> [0.8, 0.2]
# "Apple" -> [-0.5, -0.5] (Far away)

def cosine_similarity(v1, v2):
    # 1. Dot Product
    dot = sum(a*b for a, b in zip(v1, v2))
    # 2. Magnitude (Length)
    mag1 = math.sqrt(sum(a*a for a in v1))
    mag2 = math.sqrt(sum(b*b for b in v2))
    
    if mag1 == 0 or mag2 == 0: return 0
    return dot / (mag1 * mag2)

if __name__ == "__main__":
    # Simplified 2D vectors for demo
    embeddings = {
        "Puppy": [0.90, 0.95],
        "Dog":   [0.85, 0.90],
        "Kitten":[0.90, 0.92],
        "Car":   [-0.8, 0.1],  # Unrelated
        "Truck": [-0.7, 0.2]
    }
    
    query = "Puppy"
    target_vec = embeddings[query]
    
    print(f"--- 🔍 Searching for similar words to '{query}' ---")
    results = []
    
    for word, vec in embeddings.items():
        if word == query: continue
        sim = cosine_similarity(target_vec, vec)
        results.append((word, sim))
    
    # Sort by similarity
    results.sort(key=lambda x: x[1], reverse=True)
    
    for word, score in results:
        bar = "█" * int(score * 10) if score > 0 else ""
        print(f"Word: {word:10} | Similarity: {score:.5f} | {bar}")
        
    print("\n🏆 Insight: 'Dog' and 'Kitten' are close (High +Score). 'Car' is far (Negative).")

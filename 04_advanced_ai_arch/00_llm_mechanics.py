# 00_llm_mechanics.py
import random

# ==========================================
# 🤖 LLM MECHANICS: NEXT TOKEN PREDICTION
# ==========================================
# An LLM is just a giant probability machine.
# Input: "The quick brown"
# Output Probabilities: {"fox": 0.8, "bear": 0.1, "table": 0.001 ...}

vocab = ["fox", "bear", "wolf", "robot", "pizza"]
probabilities = [0.70,  0.15,   0.10,   0.04,    0.01] # Must sum to ~1.0

def predict_next_token(temperature=1.0):
    # Temperature: Controls Randomness.
    # Low Temp (0.1) -> Makes "fox" (0.7) -> 0.99. (Exaggerates winners).
    # High Temp (2.0) -> Flattens curve. "robot" has a chance.
    
    # 1. Apply Temp
    adjusted_probs = [p ** (1/temperature) for p in probabilities]
    
    # 2. Normalize
    total = sum(adjusted_probs)
    final_probs = [p / total for p in adjusted_probs]
    
    # 3. Sample
    choice = random.choices(vocab, weights=final_probs, k=1)[0]
    return choice, final_probs

if __name__ == "__main__":
    prompt = "The quick brown..."
    
    print(f"Prompt: '{prompt}'")
    print(f"Base Probs: {list(zip(vocab, probabilities))}\n")
    
    print("--- 🥶 Low Temp (0.1) - Deterministic ---")
    for _ in range(5):
        token, _ = predict_next_token(0.1)
        print(f"Generated: {token}")
        
    print("\n--- 🥵 High Temp (2.0) - Creative/Crazy ---")
    for _ in range(5):
        token, _ = predict_next_token(2.0)
        print(f"Generated: {token}")

    print("\n🏆 Insight: LLMs don't 'know' facts. They roll dice based on patterns.")

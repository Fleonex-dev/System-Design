# 05_reasoning_search.py
import time
import random

# ==========================================
# 🛑 THE SCREW UP (System 1 / Zero-Shot)
# ==========================================
# SCENARIO: Complex Math or Logic.
# LLM tries to answer immediately token-by-token.
# Usually fails because it can't "backtrack" or "plan".

def solve_zero_shot(problem):
    print(f"🛑 [System 1] Guessing answer for '{problem}'...")
    # Simulating a hallucination or wrong guess
    return "The answer is 42."

def run_the_screwup():
    problem = "Solve 24 game for inputs [5, 5, 5, 1]"
    ans = solve_zero_shot(problem)
    print(f"🛑 Result: {ans} (Likely Incorrect)")


# ==========================================
# ✅ THE FIX (System 2 / Tree of Thoughts)
# ==========================================
# SCENARIO: Use the LLM to generate multiple "next steps".
# Score them. Keep the best ones. Deep Search.
# This mimics "Thinking" (O1-preview).

class Thought:
    def __init__(self, content, score):
        self.content = content
        self.score = score

class TreeOfThoughts:
    def generate_thoughts(self, current_state):
        # Simulating LLM generating 3 possible next steps
        options = [
            f"{current_state} -> Try option A",
            f"{current_state} -> Try option B",
            f"{current_state} -> Try option C"
        ]
        return [Thought(opt, random.random()) for opt in options]
        
    def search(self, problem):
        print(f"✅ [System 2] Thinking deep about '{problem}'...")
        current_state = "Start"
        
        # Depth 3 search
        for depth in range(3):
            print(f"   Step {depth+1}: Generatng thoughts...")
            thoughts = self.generate_thoughts(current_state)
            
            # Filter/Prune (Keep top 1)
            best = max(thoughts, key=lambda t: t.score)
            print(f"   -> Selected best path: '{best.content}' (Score: {best.score:.2f})")
            current_state = best.content
            time.sleep(0.1)
            
        return f"Solved via path: {current_state}"

def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (Tree of Thoughts) ---")
    solver = TreeOfThoughts()
    ans = solver.search("Solve 24 game for inputs [5, 5, 5, 1]")
    print(f"✅ Result: {ans}")

if __name__ == "__main__":
    print("🧪 REASONING TEST: Zero-Shot (Bad) vs Tree of Thoughts (Good)\n")
    run_the_screwup()
    run_the_fix()
    
    print("\n🏆 Conclusion: For complex tasks, trade inference time for accuracy (Test-time compute).")

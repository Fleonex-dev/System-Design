# 04_mixture_of_experts.py
import time

# ==========================================
# 🛑 THE SCREW UP (Dense Model)
# ==========================================
# SCENARIO: A 100B parameter model.
# Every time you ask "Hello", ALL 100B parameters activate.
# It costs huge VRAM and Compute.

class DenseLLM:
    def forward(self, x):
        print(f"🛑 [Bad] Activating entire 100B network for input '{x}'...")
        time.sleep(0.5) # Expensive!
        return "response"

def run_the_screwup():
    llm = DenseLLM()
    llm.forward("Hello")


# ==========================================
# ✅ THE FIX (Sparse MoE)
# ==========================================
# SCENARIO: We break the model into 4 Experts (History, Math, Code, Chat).
# A "Router" decides which expert handles the query.
# For "Hello", we only use the Chat expert (25B params).
# We save 75% compute!

class Expert:
    def __init__(self, name):
        self.name = name
    def forward(self, x):
        print(f"   -> Expert[{self.name}] Processing...")
        time.sleep(0.1) # Fast

class MoERouter:
    def __init__(self):
        self.experts = {
            "math": Expert("Math"),
            "code": Expert("Code"),
            "chat": Expert("Chat"),
            "hist": Expert("History")
        }
        
    def route(self, x):
        # In reality, this is a Learned Gate (Softmax)
        if "solve" in x or "+" in x: return ["math"]
        if "def " in x: return ["code"]
        return ["chat"]

class SparseMoE:
    def __init__(self):
        self.router = MoERouter()
        
    def forward(self, x):
        print(f"✅ [MoE] Routing input '{x}'...")
        selected_keys = self.router.route(x)
        
        results = []
        for key in selected_keys:
            results.append(self.router.experts[key].forward(x))
        return results

def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (MoE) ---")
    moe = SparseMoE()
    
    # Only activates Chat Expert
    moe.forward("Hello there")
    
    # Only activates Math Expert
    moe.forward("solve 2+2")

if __name__ == "__main__":
    print("🧪 ARCH TEST: Dense (Bad) vs MoE (Good)\n")
    run_the_screwup()
    run_the_fix()
    
    print("\n🏆 Conclusion: MoE gives you GPT-4 performance at 1/10th the inference cost.")

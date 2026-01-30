# ==========================================
# 💀 THE CHALLENGE: BUILD AGI (Prototype)
# ==========================================
# SCENARIO: 
# You have a dumb chatbot `SimpleBot`.
# It cannot search memory (RAG).
# It cannot think (Reasoning).
# It runs monolithic (No Experts).
#
# GOAL:
# Upgrade `AGI_Prototype` in `challenge_solution.py` to:
# 1. Use a `Memory` class (Mock RAG).
# 2. Use a `Planner` class (Mock Reasoning/CoT).
# 3. Use an `ExpertRouter` (Mock MoE).

class SimpleBot:
    def chat(self, user_input):
        # 1. No Context
        # 2. Immediate Answer
        # 3. Single Model
        return f"I am a dumb bot. You said: {user_input}"

if __name__ == "__main__":
    print("💀 Running Dumb Bot...")
    bot = SimpleBot()
    print(bot.chat("How do I build a rocket?"))

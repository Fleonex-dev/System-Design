# 02_agent_orchestrator.py
import random

# ==========================================
# 🛑 THE SCREW UP (ReAct Loops)
# ==========================================
# SCENARIO: An agent decides what to do next.
# Thought: "I need data." Action: Search. Result: "Error 500".
# Thought: "I need data." Action: Search. Result: "Error 500".
# ... Infinite Loop.

class LoopyAgent:
    def run(self):
        print("🛑 [Bad] Starting ReAct loop...")
        for _ in range(5):
            print("Action: Search Google (Error)")
            # No state management to realize it's stuck
        
def run_the_screwup():
    LoopyAgent().run()
    print("🛑 Agent got stuck repeating actions.")


# ==========================================
# ✅ THE FIX (State Machine / DAG)
# ==========================================
# SCENARIO: Define a Graph.
# Start -> Search -> (if error) -> Retry -> (if error) -> Abort.
# Explicit transitions prevent loops.

class StateGraph:
    def __init__(self):
        self.state = "START"
        self.retries = 0
        
    def step(self):
        print(f"✅ [Graph] Current State: {self.state}")
        
        if self.state == "START":
            self.state = "SEARCH"
            
        elif self.state == "SEARCH":
            # Simulate Failure
            print("   (Simulating Search Failure...)")
            self.state = "HANDLE_ERROR"
            
        elif self.state == "HANDLE_ERROR":
            self.retries += 1
            if self.retries > 1:
                print("   Too many retries. Moving to END.")
                self.state = "END"
            else:
                print("   Retrying...")
                self.state = "SEARCH"
                
        elif self.state == "END":
            return "DONE"
            
        return "RUNNING"

def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (DAG / Graph) ---")
    graph = StateGraph()
    while True:
        status = graph.step()
        if status == "DONE":
            break
            
if __name__ == "__main__":
    print("🧪 AGENT TEST: Loop (Bad) vs DAG (Good)\n")
    run_the_screwup()
    run_the_fix()
    print("\n🏆 Conclusion: Production Agents need explicit State Machines (like LangGraph).")

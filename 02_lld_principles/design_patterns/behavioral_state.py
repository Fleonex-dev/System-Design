# behavioral_state.py
from abc import ABC, abstractmethod

# ==========================================
# 🔄 STATE PATTERN
# ==========================================
# SCENARIO: An AI Agent acts differently based on its state.
# "Thinking" -> Does not accept input.
# "Ready" -> Accepts input.
# "ToolUse" -> Waiting for Tool output.
#
# BAD: `if state == 'Thinking': ... elif ...`
# GOOD: Classes representing states.

class AgentState(ABC):
    @abstractmethod
    def handle_input(self, agent, user_input): pass

class ReadyState(AgentState):
    def handle_input(self, agent, user_input):
        print(f"   🟢 [Ready] User said: '{user_input}'. Switching to Thinking...")
        agent.set_state(ThinkingState())

class ThinkingState(AgentState):
    def handle_input(self, agent, user_input):
        print(f"   🛑 [Thinking] Busy! Ignoring: '{user_input}'")
        # Logic to finish thinking...
        print("   ... Finished thinking. Result: 42.")
        agent.set_state(ReadyState())

class Agent:
    def __init__(self):
        self.state = ReadyState()
        
    def set_state(self, state):
        self.state = state
        
    def chat(self, msg):
        self.state.handle_input(self, msg)

if __name__ == "__main__":
    print("--- 🔄 State Pattern Demo ---")
    bot = Agent()
    
    bot.chat("Hello!") # Should work
    bot.chat("Are you there?") # Should be ignored (Thinking)
    bot.chat("Another one") # Should work (Ready again)

from abc import ABC, abstractmethod

# ==========================================
# 🛑 THE SCREW UP (The "God" Class)
# ==========================================
# SCENARIO: A single class that does:
# 1. Auth, 2. DB saving, 3. OpenAI calls, 4. JSON parsing.
# VIOLATION: Single Responsibility Principle (SRP).
# CONSEQUENCE: If you want to change the DB, you might break the LLM logic.

class GodModeBot:
    def __init__(self):
        self.db_path = "history.json"
        self.api_key = "sk-..."
    
    def chat(self, user_input):
        print("🛑 [Bad] Authenticating...")
        # LOGIC 1: Auth
        if not self.api_key: raise Exception("No Key")
        
        print("🛑 [Bad] Calling OpenAI...")
        # LOGIC 2: LLM Call
        response = f"Simulated Response to {user_input}"
        
        print("🛑 [Bad] Saving to DB...")
        # LOGIC 3: Database
        with open(self.db_path, "a") as f:
            f.write(f"{user_input}:{response}\n")
            
        return response

def run_the_screwup():
    print("\n--- 🛑 Running BAD implementation (God Object) ---")
    bot = GodModeBot()
    bot.chat("Hello!")


# ==========================================
# ✅ THE FIX (S.O.L.I.D)
# ==========================================
# 1. SRP: Separate storage, LLM, and orchestration.
# 2. DIP: Agent depends on Abstractions (interfaces), not concrete details.

# --- Abstractions (Interfaces) ---
class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str: pass

class Storage(ABC):
    @abstractmethod
    def save(self, user: str, ai: str): pass

# --- Concrete Implementations ---
class OpenAIProvider(LLMProvider):
    def generate(self, prompt: str) -> str:
        print("✅ [Good] Calling OpenAI API...")
        return f"GPT says: {prompt}"

class LocalStorage(Storage):
    def save(self, user: str, ai: str):
        print(f"✅ [Good] Saved chat to local file.")

# --- The Agent (Orchestrator only) ---
class Agent:
    def __init__(self, llm: LLMProvider, storage: Storage):
        # Dependency Injection! (DIP)
        # We don't care WHICH LLM or WHICH Storage, as long as they fit the interface.
        self.llm = llm
        self.storage = storage

    def run(self, input_text):
        response = self.llm.generate(input_text)
        self.storage.save(input_text, response)
        return response

def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (SOLID) ---")
    
    # We can swap these out easily!
    llm = OpenAIProvider()
    db = LocalStorage()
    
    agent = Agent(llm, db)
    agent.run("Hello SOLID!")

if __name__ == "__main__":
    print("🧪 SOLID TEST: God Object (Bad) vs Modular Agent (Good)\n")
    run_the_screwup()
    run_the_fix()
    
    print("\n🏆 Conclusion: SOLID lets you swap components (e.g., switch to Anthropic) without touching the Agent code.")

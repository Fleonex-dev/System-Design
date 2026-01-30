from abc import ABC, abstractmethod

# ==========================================
# 🛑 THE SCREW UP (Conditional Spaghetti)
# ==========================================
# SCENARIO: You start with only OpenAI.
# Then you add Anthropic. Then LLaMA. Then Mistral.
# You end up with 50 if-else statements scattered across your codebase.

class ChatAppBad:
    def generate_response(self, provider, text):
        print(f"🛑 [Bad] Requesting {provider}...")
        
        # LOGIC PLACED EVERYWHERE
        if provider == "openai":
            return f"GPT-4 response to '{text}'"
        elif provider == "anthropic":
            return f"Claude response to '{text}'"
        elif provider == "llama":
            return f"Llama3 response to '{text}'"
        else:
            raise ValueError("Unknown provider")

def run_the_screwup():
    app = ChatAppBad()
    print(app.generate_response("openai", "Hello"))
    print(app.generate_response("anthropic", "Hi"))


# ==========================================
# ✅ THE FIX (Factory Pattern)
# ==========================================
# SCENARIO: Centralize object creation.
# If you add a new provider, you only touch the Factory.
# The rest of the app doesn't know (or care) which class it's using.

# Interface
class LLM(ABC):
    @abstractmethod
    def complete(self, text: str) -> str: pass

# Concrete Products
class OpenAILLM(LLM):
    def complete(self, text: str): return f"GPT-4: {text}"

class AnthropicLLM(LLM):
    def complete(self, text: str): return f"Claude-3: {text}"

class LocalLLM(LLM):
    def complete(self, text: str): return f"Llama-3 (Local): {text}"

# THE FACTORY
class LLMFactory:
    @staticmethod
    def get_llm(provider_name: str) -> LLM:
        registry = {
            "openai": OpenAILLM,
            "anthropic": AnthropicLLM,
            "local": LocalLLM
        }
        
        provider_class = registry.get(provider_name.lower())
        if not provider_class:
            raise ValueError(f"Unknown provider: {provider_name}")
            
        return provider_class()

def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (Factory) ---")
    
    # Client code is clean. It just asks for an object.
    my_llm = LLMFactory.get_llm("anthropic")
    print(f"✅ Created class type: {type(my_llm).__name__}")
    print(my_llm.complete("Hello Pattern"))
    
    # Easy to switch via config string
    my_llm_2 = LLMFactory.get_llm("local")
    print(my_llm_2.complete("Hello Local"))

if __name__ == "__main__":
    print("🧪 FACTORY TEST: If/Else (Bad) vs Factory (Good)\n")
    run_the_screwup()
    run_the_fix()
    
    print("\n🏆 Conclusion: Adding a new model? Just update the Factory registry. No broken if-statements.")

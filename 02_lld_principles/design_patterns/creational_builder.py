# creational_builder.py
from typing import List, Optional

# ==========================================
# 🏗️ BUILDER PATTERN
# ==========================================
# SCENARIO: Creating an `LLMRequest` is complex.
# It has 20 optional parameters (temperature, top_k, tools, stop_sequences...).
# A constructor with 20 args is messy: `LLM(0.7, None, [], True, ...)` -> What is True?
# 
# The Builder makes it readable: `LLM.builder().set_temp(0.7).enable_stream().build()`

class LLMConfig:
    def __init__(self, model, temp, stream, tools):
        self.model = model
        self.temp = temp
        self.stream = stream
        self.tools = tools
    
    def __str__(self):
        return f"🤖 Config(Model={self.model}, Temp={self.temp}, Stream={self.stream}, Tools={len(self.tools)})"

class LLMBuilder:
    def __init__(self):
        # Default values
        self.model = "gpt-4"
        self.temp = 0.0
        self.stream = False
        self.tools = []
        
    def set_model(self, model):
        self.model = model
        return self # Fluent Interface
        
    def set_temperature(self, temp):
        self.temp = temp
        return self
        
    def enable_streaming(self):
        self.stream = True
        return self
        
    def add_tool(self, tool_name):
        self.tools.append(tool_name)
        return self
        
    def build(self):
        # Validation logic can go here
        if self.temp > 2.0: raise ValueError("Temp too high!")
        return LLMConfig(self.model, self.temp, self.stream, self.tools)

if __name__ == "__main__":
    print("--- 🏗️ Builder Pattern Demo ---")
    
    # Fluent API (Method Chaining)
    config = (LLMBuilder()
              .set_model("claude-3")
              .set_temperature(0.7)
              .enable_streaming()
              .add_tool("web_search")
              .add_tool("calculator")
              .build())
              
    print(config)
    print("\n✅ Benefits: Readable code. No massive constructors. Immutable result.")

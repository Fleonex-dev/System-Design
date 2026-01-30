# 03_lora_adapters.py
import random

# ==========================================
# 🎭 LoRA (Low-Rank Adaptation)
# ==========================================
# SCENARIO: You serve users from Legal, Medical, and Coding domains.
# BAD: Load 3 copies of GPT-4 (Trillions of params). Memory OOM.
# GOOD: Load 1 Base Model (Frozen) + 3 Tiny Adapters (LoRA).
#
# Math: Result = Base(x) + Adapter(x)

class BaseModel:
    def predict(self, input_vec):
        # Heavy computation (Simulated)
        return sum(input_vec) 

class LoRA_Adapter:
    def __init__(self, name, bias):
        self.name = name
        self.bias = bias # Simplified Weight Matrix A*B
        
    def forward(self, input_vec):
        return sum(input_vec) * self.bias

def inference(input_data, adapter_name):
    # 1. Base Model Output (Shared)
    base_out = BaseModel().predict(input_data)
    
    # 2. Adapter Output (Specific)
    adapter_out = 0
    if adapter_name == "legal":
        adapter_out = LoRA_Adapter("Legal", 0.5).forward(input_data)
    elif adapter_name == "code":
        adapter_out = LoRA_Adapter("Code", 2.0).forward(input_data)
        
    # 3. Combine
    return base_out + adapter_out

if __name__ == "__main__":
    print("--- 🎭 Multi-Tenant LoRA Serving ---")
    input_vec = [1.0, 2.0, 3.0] # "How do I sue someone?"
    
    print(f"Input: {input_vec}")
    
    # Request 1: Legal Client
    res_legal = inference(input_vec, "legal")
    print(f"Legal Output: {res_legal:.2f} (Base + 0.5x)")
    
    # Request 2: Coding Client
    res_code = inference(input_vec, "code")
    print(f"Code Output:  {res_code:.2f} (Base + 2.0x)")
    
    print("\n🏆 Insight: Swapping LoRA adapters takes milliseconds. Swapping full models takes minutes.")

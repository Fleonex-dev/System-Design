# 01_quantization.py
import random
import sys

# ==========================================
# 📉 AI OPTIMIZATION: QUANTIZATION
# ==========================================
# Scenario: Converting FP32 (32-bit floats) to INT8 (8-bit integers).
# Why? 4x Memory Reduction, Faster Math.
# Cost? Precision Loss.

def simulate_quantization():
    print("--- 📉 Quantization Demo (FP32 -> INT8) ---")
    
    # 1. Weights in FP32 (Simulated)
    # Range -1.0 to 1.0 is typical for Neural Nets
    weights_fp32 = [0.123456789, -0.987654321, 0.000000001, 0.555555555]
    
    print(f"FP32 Weights: {weights_fp32}")
    size_fp32 = len(weights_fp32) * 4 # 4 bytes per float
    print(f"Memory: {size_fp32} bytes")
    
    # 2. Quantize to INT8 (-127 to 127)
    # Formula: int( val / max_abs_val * 127 )
    max_val = max(abs(w) for w in weights_fp32)
    s = 127 / max_val # Scale factor
    
    weights_int8 = [int(w * s) for w in weights_fp32]
    print(f"\nINT8 Weights: {weights_int8}")
    size_int8 = len(weights_int8) * 1 # 1 byte per int
    print(f"Memory: {size_int8} bytes (75% Reduction!)")
    
    # 3. De-Quantize (Inference)
    # Formula: int_val / s
    weights_restored = [w / s for w in weights_int8]
    print(f"\nRestored:    {weights_restored}")
    
    # 4. Error Analysis
    print("\n--- 🔍 Error Analysis ---")
    for orig, new in zip(weights_fp32, weights_restored):
        err = abs(orig - new)
        print(f"Orig: {orig: .9f} | Rec: {new: .9f} | Err: {err:.9f}")
        
    print("\n🏆 Conclusion: Small precision loss, HUGE speed/memory gain.")

if __name__ == "__main__":
    simulate_quantization()

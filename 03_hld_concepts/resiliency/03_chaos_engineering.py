# 03_chaos_engineering.py
import random
import time

# ==========================================
# 🐒 CHAOS ENGINEERING (Netflix)
# ==========================================
# SCENARIO: Your system looks fine.
# But what if `get_database()` suddenly sleeps for 10s?
# Chaos Monkey RANDOMLY injects failure to force you to handle it.

class ChaosMonkey:
    def __init__(self, probability=0.3):
        self.prob = probability
        
    def attack(self, func_name):
        if random.random() < self.prob:
            attack_type = random.choice(["latency", "exception", "kill"])
            print(f"\n   🐵 CHAOS MONKEY ATTACK! [{attack_type}] on {func_name}")
            
            if attack_type == "latency":
                time.sleep(1) # Simulated network lag
            elif attack_type == "exception":
                raise ConnectionError("Network Partition")
            elif attack_type == "kill":
                raise SystemExit("Service Killed")

monkey = ChaosMonkey(probability=0.5)

def sensitive_operation():
    # Inject Chaos
    monkey.attack("SensitiveOp")
    print("   ✅ Operation Success.")

def robust_system():
    print("--- 🛡️ Resilient System ---")
    try:
        sensitive_operation()
    except ConnectionError:
        print("   ⚠️  Caught Network Partition! Retrying... (Resilience)")
    except SystemExit:
        print("   ⚠️  Service Restarting... (Self-Healing)")
    except Exception as e:
        print(f"   ⚠️  Unknown Error: {e}")

if __name__ == "__main__":
    print("--- 🐒 Chaos Engineering Demo ---")
    
    for i in range(5):
        print(f"Run {i}: ", end="")
        robust_system()
        
    print("\n🏆 Insight: If you don't test failure, you will fail in production.")
    print("   🏢 Real World: **Netflix Chaos Monkey** kills AWS EC2 instances randomly during business hours.")
    print("   **Gremlin** is a generic Chaos-as-a-Service platform.")

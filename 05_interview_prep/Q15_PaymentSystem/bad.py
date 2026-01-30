# bad.py
import random

# ==========================================
# 🛑 BAD: RETRY WITHOUT IDEMPOTENCY
# ==========================================
# SCENARIO: Charging user $10.
# Action: Call Bank API.
# Result: Timeout.
# Naive Response: Retry.
#
# DANGER: What if the first request actually succeeded but response was lost?
# User gets charged twice!

class Bank:
    def __init__(self):
        self.balance = 100
        
    def charge(self, amount):
        # Simulate network flake
        if random.random() < 0.5:
            raise TimeoutError("Timeout")
        self.balance -= amount
        print(f"   💰 Charged ${amount}. New Bal: {self.balance}")

if __name__ == "__main__":
    bank = Bank()
    # Retry Logic
    try:
        bank.charge(10)
    except:
        print("   ⚠️ Timeout. Retrying...")
        bank.charge(10) # DANGER

# 00_oop_primer.py
from abc import ABC, abstractmethod

# ==========================================
# 🏗️ LLD PRIMER: INTERFACES & POLYMORPHISM
# ==========================================
# Before SOLID, we must understand Interfaces (Contracts).
# A Class 'signs a contract' to implement methods.

# 1. The Contract (Abstract Base Class)
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: int):
        pass
    
    @abstractmethod
    def refund(self, amount: int):
        pass

# 2. Implementation A (Stripe)
class Stripe(PaymentProcessor):
    def pay(self, amount):
        print(f"✅ [Stripe] Charged ${amount}")
        
    def refund(self, amount):
        print(f"↩️ [Stripe] Refunded ${amount}")

# 3. Implementation B (PayPal)
class PayPal(PaymentProcessor):
    def pay(self, amount):
        print(f"✅ [PayPal] Charged ${amount}")
        
    def refund(self, amount):
        print(f"↩️ [PayPal] Refunded ${amount}")

# 4. Polymorphism (The Magic)
# The `checkout` function DOES NOT CARE if it is Stripe or PayPal.
# It only cares that it implements `pay()`.
def checkout(processor: PaymentProcessor, cost: int):
    print("🛒 Processing Cart...")
    processor.pay(cost)

if __name__ == "__main__":
    print("--- 🏗️ OOP Polymorphism Demo ---")
    s = Stripe()
    p = PayPal()
    
    # Interchangeable!
    checkout(s, 100)
    checkout(p, 50)
    
    # This separation allows us to swap Stripe -> PayPal without breaking the Checkout code.
    # This is the heart of LLD.

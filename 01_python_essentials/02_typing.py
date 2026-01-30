from typing import List, Optional
from pydantic import BaseModel, ValidationError

# ==========================================
# 🛑 THE SCREW UP (Unstructured Dicts)
# ==========================================
# SCENARIO: You are processing a webhook payload from a payment provider.
# You use raw dictionaries. It works fine for 6 months.
# Then, the provider changes "amount" (float) to "amount_cents" (int).
# Your code crashes in production on a Friday night.

def process_payment_bad(payload: dict):
    print("\n🛑 [Bad] Processing payment...")
    try:
        # 1. No autocomplete. You have to remember if it's 'user_id' or 'userId'
        user = payload['user_id']
        
        # 2. No implementation of type checks. 'amount' could be a string "10.00"
        amount = payload['amount'] 
        
        # 3. Silent failure risk. If 'currency' is missing, it crashes here.
        currency = payload['currency']
        
        print(f"🛑 charged {amount} {currency} to {user}")
        
    except KeyError as e:
        print(f"🛑 CRITICAL ERROR: Missing field {e}")
    except Exception as e:
        print(f"🛑 CRITICAL ERROR: {e}")

def run_the_screwup():
    # Good payload
    process_payment_bad({"user_id": "u123", "amount": 100.0, "currency": "USD"})
    
    # Bad payload (Typos, missing fields) - SIMULATING A BUG
    # "tgt" instead of "user_id"
    process_payment_bad({"tgt": "u123", "amount": 100.0})


# ==========================================
# ✅ THE FIX (Pydantic Models)
# ==========================================
# SCENARIO: We define a strict schema. 
# Data is validated AT THE DOOR. If it's garbage, we reject it immediately.
# We get autocomplete and type safety.

class Payment(BaseModel):
    user_id: str
    amount: float
    currency: str = "USD" # Default value!
    
    # You can even add custom validators
    # @validator('amount') ...

def process_payment_good(payload: dict):
    print("\n✅ [Good] Processing payment...")
    try:
        # Validates data. Converts types (e.g., string "100.5" -> float 100.5)
        payment = Payment(**payload)
        
        # Look at this beautiful autocomplete support (in IDE)
        print(f"✅ charged {payment.amount} {payment.currency} to {payment.user_id}")
        
    except ValidationError as e:
        print(f"✅ Blocked Bad Data:\n{e.json(indent=2)}")

def run_the_fix():
    # Good payload
    process_payment_good({"user_id": "u123", "amount": 100.0, "currency": "USD"})
    
    # Bad payload (Typos, wrong types)
    # Pydantic will catch 'tgt' (extra field) and missing 'user_id'
    process_payment_good({"tgt": "u123", "amount": "not_a_number"})


if __name__ == "__main__":
    print("🧪 TYPING TEST: Dicts (Bad) vs Pydantic (Good)\n")
    
    run_the_screwup()
    run_the_fix()
    
    print("\n🏆 Conclusion: Pydantic crashes EARLY (good). Dicts crash LATE (bad).")

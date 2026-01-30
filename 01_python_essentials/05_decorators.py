import time
import functools

# ==========================================
# 🛑 THE SCREW UP (Boilerplate Hell)
# ==========================================
# SCENARIO: You want to measure performance of your 10 critical functions.
# You copy-paste the timing code into every single one.
# If you want to change logging to a file later, you have to edit 10 places.

def process_data_bad(data):
    start = time.time() # <--- Boilerplate
    print("🛑 [Bad] Processing data...")
    time.sleep(0.5) 
    end = time.time()   # <--- Boilerplate
    print(f"🛑 Execution time: {end - start:.4f}s") # <--- Boilerplate
    return data * 2

def send_email_bad(email):
    start = time.time() # <--- Boilerplate
    print(f"🛑 [Bad] Sending email to {email}...")
    time.sleep(0.3)
    end = time.time()   # <--- Boilerplate
    print(f"🛑 Execution time: {end - start:.4f}s") # <--- Boilerplate
    return True

def run_the_screwup():
    print("\n--- 🛑 Running BAD implementation (Boilerplate) ---")
    process_data_bad(100)
    send_email_bad("test@example.com")


# ==========================================
# ✅ THE FIX (Decorators)
# ==========================================
# SCENARIO: We write the logic ONCE.
# We "wrap" any function we want with @measure_time.
# The code is clean, reusable, and follows DRY (Don't Repeat Yourself).

def measure_time(func):
    """A decorator that measures how long a function takes to run."""
    @functools.wraps(func) # Preserves the original function's name/docstring
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"✅ [{func.__name__}] executed in {end - start:.4f}s")
        return result
    return wrapper

@measure_time
def process_data_good(data):
    print("✅ [Good] Processing data...")
    time.sleep(0.5)
    return data * 2

@measure_time
def send_email_good(email):
    print(f"✅ [Good] Sending email to {email}...")
    time.sleep(0.3)
    return True

def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (Decorators) ---")
    process_data_good(100)
    send_email_good("test@example.com")

if __name__ == "__main__":
    print("🧪 DECORATOR TEST: Copy-Paste (Bad) vs @Decorator (Good)\n")
    
    run_the_screwup()
    run_the_fix()
    
    print("\n🏆 Conclusion: Decorators separate 'Business Logic' from 'Infrastructure Logic' (Logging, Auth, Retry).")

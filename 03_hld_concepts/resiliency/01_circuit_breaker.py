# 01_circuit_breaker.py
import time
import random

# ==========================================
# ⚡ CIRCUIT BREAKER
# ==========================================
# SCENARIO: Service A calls Service B. Service B is down.
# Naive approach: Keep calling (Timeouts stack up, Main thread blocked).
# Result: Cascade Failure.
#
# Solution: "Trip the breaker". Stop calling B for a while. Return error immediately.

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=2):
        self.state = "CLOSED" # CLOSED (Good), OPEN (Bad), HALF-OPEN (Testing)
        self.failures = 0
        self.threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = 0
        
    def call(self, service_func):
        if self.state == "OPEN":
            # Check if timeout passed
            if time.time() - self.last_failure_time > self.recovery_timeout:
                print("   ⚠️  [Breaker] Timeout passed. Switching to HALF-OPEN (Test Drive)...")
                self.state = "HALF-OPEN"
            else:
                print("   ❌ [Breaker] OPEN. Fast Fail! (Saving Resources)")
                return False

        try:
            # Try to call service
            result = service_func()
            
            if self.state == "HALF-OPEN":
                print("   ✅ [Breaker] HALF-OPEN Success! Closing Circuit.")
                self.state = "CLOSED"
                self.failures = 0
            return result
            
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            print(f"   🔥 [Breaker] Call Failed! ({self.failures}/{self.threshold})")
            
            if self.failures >= self.threshold:
                print("   💥 [Breaker] Threshold reached. TRIPPING CIRCUIT (OPEN)!")
                self.state = "OPEN"
            return False

# Flaky Service simulation
def risky_service():
    if random.random() < 0.7:
        raise ConnectionError("Service Down")
    return "Success"

def run_simulation():
    print("--- ⚡ Circuit Breaker Simulation ---")
    cb = CircuitBreaker()
    
    for i in range(10):
        print(f"\nRequest {i+1}:")
        cb.call(risky_service)
        time.sleep(0.5)

if __name__ == "__main__":
    run_simulation()

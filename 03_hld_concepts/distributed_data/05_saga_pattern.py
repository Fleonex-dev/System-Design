# 05_saga_pattern.py
import time

# ==========================================
# 🦅 SAGA PATTERN (Distributed Transactions)
# ==========================================
# SCENARIO: Booking a Trip (Flight + Hotel).
# Service A: Book Flight.
# Service B: Book Hotel.
#
# If Hotel fails, Flight MUST be cancelled (Compensated).
# We cannot use a Database Lock across two different Services.

class Service:
    def __init__(self, name, fail_rate=0.0):
        self.name = name
        self.fail_rate = fail_rate
        
    def execute(self):
        print(f"   ▶️  [{self.name}] Executing...")
        if time.time() % 1 > (1.0 - self.fail_rate): # Deterministic randomness based on time
            raise Exception("Service Failure")
        print(f"   ✅ [{self.name}] Success.")
        return True
        
    def compensate(self):
        print(f"   ↩️  [{self.name}] COMPENSATING (Undo Action).")

class SagaOrchestrator:
    def __init__(self):
        self.steps = [] # tuples of (service, undo_func)
        
    def add_step(self, service):
        self.steps.append(service)
        
    def run(self):
        executed = []
        try:
            for service in self.steps:
                service.execute()
                executed.append(service)
                
            print("\n🎉 SAGA COMPLETE! Trip Booked.")
            
        except Exception as e:
            print(f"   🔥 Error: {e}")
            print("   ⚠️  Triggering Rollback Pattern...")
            
            # Rollback in reverse order
            for service in reversed(executed):
                service.compensate()
            
            print("❌ SAGA FAILED (Clean State Restored).")

if __name__ == "__main__":
    print("--- 🦅 Saga Pattern Demo (Amazon) ---")
    
    # Happy Path
    print("\n1. Happy Path:")
    saga = SagaOrchestrator()
    saga.add_step(Service("Book Flight"))
    saga.add_step(Service("Book Hotel"))
    saga.add_step(Service("Charge Card"))
    saga.run()
    
    # Failure Path
    print("\n2. Failure Simulation:")
    saga_fail = SagaOrchestrator()
    saga_fail.add_step(Service("Book Flight"))
    saga_fail.add_step(Service("Book Hotel", fail_rate=1.0)) # Fail here
    saga_fail.add_step(Service("Charge Card"))
    saga_fail.run()
    
    print("\n🏆 Insight: Sagas allow 'ACID-like' properties across Microservices.")
    print("   🏢 Real World: **Uber Eats** (Order -> Restaurant Accept -> Driver Assign).")
    print("   **Amazon** uses this for almost every order (Inventory -> Payment -> Shipping).")

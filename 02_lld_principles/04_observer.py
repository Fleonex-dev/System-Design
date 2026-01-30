import time

# ==========================================
# 🛑 THE SCREW UP (Polling)
# ==========================================
# SCENARIO: You have a long-running Agent job (takes 10s).
# The UI needs to know when it finishes.
# The UI constantly asks "Are you done?" "Are you done?"
# This wastes CPU and Network.

class JobBad:
    def __init__(self):
        self.status = "running"
        
    def check_status(self):
        # Simulating random completion
        if int(time.time()) % 2 == 0:
            self.status = "completed"
        return self.status

def run_the_screwup():
    print("🛑 [Bad] Polling for status...")
    job = JobBad()
    
    # Busy waiting loop
    while True:
        status = job.check_status()
        print(f"🛑 Polling... Status: {status}")
        if status == "completed":
            print("🛑 Finally done!")
            break
        time.sleep(1)


# ==========================================
# ✅ THE FIX (Observer Pattern)
# ==========================================
# SCENARIO: Don't call us, we'll call you.
# The Job (Subject) maintains a list of Subscribers (Observers).
# When state changes, it notifies them.

class Observer:
    def update(self, status):
        print(f"✅ [Observer] Recieved update: Job is {status}!")

class JobSubject:
    def __init__(self):
        self._observers = []
        self._status = "running"
        
    def attach(self, observer):
        self._observers.append(observer)
        
    def set_status(self, new_status):
        print(f"✅ [Subject] Status changed to {new_status}")
        self._status = new_status
        self._notify()
        
    def _notify(self):
        for observer in self._observers:
            observer.update(self._status)

def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (Observer) ---")
    
    job = JobSubject()
    ui_subscriber = Observer()
    logger_subscriber = Observer()
    
    job.attach(ui_subscriber)
    job.attach(logger_subscriber)
    
    # Simulate work
    time.sleep(1)
    job.set_status("processing_chunk_1")
    
    time.sleep(1)
    job.set_status("completed")

if __name__ == "__main__":
    print("🧪 OBSERVER TEST: Polling (Bad) vs Event-Driven (Good)\n")
    
    # run_the_screwup() # Commented out to save time, it's an infinite loop simulation
    print("🛑 Skipped Polling demo (it's slow).")
    
    run_the_fix()
    
    print("\n🏆 Conclusion: Event-driven architectures scale better than polling.")

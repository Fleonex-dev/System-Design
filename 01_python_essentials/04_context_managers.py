import sqlite3
import os

# ==========================================
# 🛑 THE SCREW UP (Manual Resource Management)
# ==========================================
# SCENARIO: You connect to a database.
# An error occurs halfway through your logic.
# The connection is NEVER closed.
# Result: Your DB creates "Zombie Connections" and eventually blocks new users.

def manage_db_bad():
    print("🛑 [Bad] Opening DB connection...")
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id int, name text)")
        # SIMULATING AN ERROR
        raise Exception("Something went wrong processing data!")
        
        # This line is UNREACHABLE. The connection remains open forever.
        conn.close()
        
    except Exception as e:
        print(f"🛑 Error occurred: {e}")
        print("🛑 OOPS: We forgot to close the connection in the except block!")

def run_the_screwup():
    print("\n--- 🛑 Running BAD implementation (No cleanup) ---")
    manage_db_bad()
    # At this point, the file handle 'test.db' might still be locked by the OS.


# ==========================================
# ✅ THE FIX (Context Managers / 'with')
# ==========================================
# SCENARIO: We wrap the connection in a Class that implements __enter__ and __exit__.
# No matter what happens (return, error, crash), __exit__ is called.
# This guarantees cleanup.

class ManagedDB:
    def __init__(self, filename):
        self.filename = filename
        
    def __enter__(self):
        print(f"✅ [Good] Entering Context: Connecting to {self.filename}...")
        self.conn = sqlite3.connect(self.filename)
        return self.conn
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("✅ [Good] Exiting Context: Closing connection cleanup...")
        if self.conn:
            self.conn.close()
        if exc_type:
            print(f"✅ [Good] Caught exception in __exit__: {exc_val}")
        # Return False to propagate exception, True to suppress it
        return True

def run_the_fix():
    print("\n--- ✅ Running GOOD implementation (Context Manager) ---")
    
    # Even though we crash inside, the "Exiting Context" print WILL happen.
    try:
        with ManagedDB("test.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS users (id int, name text)")
            print("✅ Executing logic...")
            raise Exception("Crash inside with block!")
            
    except Exception:
        pass # We handled it in __exit__ (by returning True) or here.
        
    print("✅ Logic continues safe and sound.")

if __name__ == "__main__":
    print("🧪 CONTEXT MANAGER TEST: Leaks (Bad) vs 'with' (Good)\n")
    
    run_the_screwup()
    run_the_fix()
    
    # Cleanup
    if os.path.exists("test.db"):
        os.remove("test.db")
    
    print("\n🏆 Conclusion: ALWAYS use 'with' for external resources (Network, files, GPUs).")

# bad.py

# ==========================================
# 🛑 BAD: GREP (Full Scan)
# ==========================================
# SCENARIO: Search 1TB of logs for "error".
# NAIVE: Iterate every line.
# PROBLEM: O(N). Extremely slow.

class LogSearch:
    def __init__(self):
        self.logs = []
        
    def search(self, query):
        print("   🐢 Scanning all logs...")
        return [l for l in self.logs if query in l]

if __name__ == "__main__":
    ls = LogSearch()
    ls.logs = ["INFO start", "ERROR db die", "INFO end"]
    print(ls.search("ERROR"))

import random
import string

# ==========================================
# 🛑 BAD SOLUTION (Random Strings)
# ==========================================
# PROBLEMS:
# 1. Collision Risk: High probability of generating duplicate generic strings.
# 2. Hard to Scale: Checking "if exists in DB" becomes slow as DB grows.

class TinyURLBad:
    def __init__(self):
        self.db = {} # In-memory map
        
    def shorten(self, url):
        # Brute force random string
        while True:
            short = ''.join(random.choices(string.ascii_letters, k=6))
            if short not in self.db:
                self.db[short] = url
                return short

if __name__ == "__main__":
    print("🛑 Generating short URLs...")
    app = TinyURLBad()
    print(app.shorten("google.com"))

# bad.py
import time

# ==========================================
# 🛑 BAD: FULL UPLOAD UPDATE
# ==========================================
# SCENARIO: You edit 1 character in a 100MB Word doc.
# NAIVE: Upload the entire 100MB file again.
#
# PROBLEM:
# 1. Bandwidth waste.
# 2. Slow sync time.
# 3. Risk of failure (long uploads fail often).

class FileStorage:
    def upload(self, filename, content):
        print(f"   🐢 Uploading '{filename}' ({len(content)} bytes)...")
        time.sleep(0.5) # Simluating big payload
        print("   ✅ Upload Complete.")

if __name__ == "__main__":
    storage = FileStorage()
    
    # Initial
    doc = "A" * 1000000
    storage.upload("thesis.doc", doc)
    
    # Small Edit
    doc += "B"
    print("\nMade 1 character change...")
    storage.upload("thesis.doc", doc) # Re-uploads EVERYTHING

# optimal.py
import hashlib

# ==========================================
# ✅ OPTIMAL: BLOCK LEVEL DEDUP
# ==========================================
# STRATEGY:
# 1. Break file into blocks (e.g., 4KB).
# 2. Hash each block.
# 3. Only upload blocks whose Hash isn't already on server.

class BlockStorage:
    def __init__(self):
        self.server_blocks = {} # Map Hash -> Content
        
    def sync_file(self, filename, content):
        # 1. Chunking
        block_size = 10
        blocks = [content[i:i+block_size] for i in range(0, len(content), block_size)]
        
        print(f"   📄 Processing '{filename}' ({len(blocks)} blocks)...")
        
        uploaded_count = 0
        for block in blocks:
            # 2. Hashing
            b_hash = hashlib.md5(block.encode()).hexdigest()
            
            # 3. Dedup check
            if b_hash not in self.server_blocks:
                print(f"      ⬆️  Uploading new block: {b_hash[:6]}...")
                self.server_blocks[b_hash] = block
                uploaded_count += 1
            else:
                print(f"      ⚡ Skipped existing block: {b_hash[:6]}")
                
        print(f"   ✅ Sync Complete. Uploaded {uploaded_count}/{len(blocks)} blocks.")

if __name__ == "__main__":
    storage = BlockStorage()
    
    # Initial
    doc = "HelloWorld" * 3
    print("--- 1. Initial Sync ---")
    storage.sync_file("thesis.doc", doc)
    
    # Edit
    print("\n--- 2. Differential Sync (Changed 1 char) ---")
    doc = "HelloWorld" * 2 + "HelloWorl!" # Changed last char
    storage.sync_file("thesis.doc", doc)
    
    print("\n🏆 Insight: By splitting files into blocks, we only send the delta.")
    print("   This is how **Dropbox** and **Google Drive** save bandwidth.")

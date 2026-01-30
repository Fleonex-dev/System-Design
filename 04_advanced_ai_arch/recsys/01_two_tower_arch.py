# 01_two_tower_arch.py
import math

# ==========================================
# 🗼 TWO TOWER ARCHITECTURE (RecSys)
# ==========================================
# Used by YouTube/Netflix/TikTok.
# Goal: Find the best video for User U from 1B Videos.
#
# Tower 1 (User): Compresses User history -> Vector U
# Tower 2 (Item): Compresses Video metadata -> Vector V
# Score = U dot V (High score = High affinity)

class UserTower:
    def encode(self, history, location):
        # Simulate Neural Net processing
        # Returns a vector based on preferences
        if "action" in history:
            return [0.9, 0.1, 0.5] # Loves Action
        else:
            return [0.1, 0.9, 0.2] # Loves Romance

class ItemTower:
    def encode(self, genre, duration):
        if genre == "action":
            return [0.85, 0.15, 0.6]
        elif genre == "romance":
            return [0.10, 0.95, 0.1]
        return [0,0,0]

def dot_product(v1, v2):
    return sum(a*b for a,b in zip(v1, v2))

if __name__ == "__main__":
    print("--- 🗼 Two-Tower RecSys ---")
    
    u_tower = UserTower()
    i_tower = ItemTower()
    
    # 1. User arrives (Loves Action)
    user_vec = u_tower.encode(history=["action", "thriller"], location="US")
    print(f"User Vector: {user_vec}")
    
    # 2. Candidate Items
    catalog = [
        {"id": 1, "genre": "action", "title": "Die Hard"},
        {"id": 2, "genre": "romance", "title": "The Notebook"}
    ]
    
    # 3. Retrieval (Dot Product)
    print("\n--- Scoring Candidates ---")
    for item in catalog:
        item_vec = i_tower.encode(item["genre"], 120)
        score = dot_product(user_vec, item_vec)
        print(f"Movie: {item['title']:15} | Vector: {item_vec} | Score: {score:.3f}")
        
    print("\n🏆 Insight: The 'Action' user has a much higher dot-product with 'Die Hard'.")
    print("   In prod, we use FAISS/Annoy to find these top matches from Billions.")
    print("   🏢 Real World: **YouTube** uses this for 'Candidate Generation' (filtering 5B videos -> 100).")
    print("   **Netflix** uses it to personalize the homepage rows. **TikTok** uses it for the 'For You' feed.")

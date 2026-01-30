# bad.py
import time

# ==========================================
# 🛑 BAD: PULL MODEL (Query Time)
# ==========================================
# SCENARIO: User opens Facebook. We need to show "Friends' Activity".
#
# NAIVE APPROACH:
# "SELECT * FROM posts WHERE user_id IN (my_friends) ORDER BY date DESC"
#
# PROBLEM:
# 1. Read heavy: If I have 1000 friends, this query scans 1000 user timelines.
# 2. Latency: User waits while DB crunches data.

class Database:
    def __init__(self):
        self.posts = [] # List of (user_id, content, timestamp)

    def add_post(self, user_id, content):
        self.posts.append({
            "user_id": user_id, 
            "content": content, 
            "time": time.time()
        })

    def get_feed(self, friend_ids):
        # ❌ EXPENSIVE QUERY ON READ
        print(f"   🐢 Querying posts for friends: {friend_ids}...")
        feed = [p for p in self.posts if p["user_id"] in friend_ids]
        feed.sort(key=lambda x: x["time"], reverse=True)
        return feed

if __name__ == "__main__":
    db = Database()
    # Writes are fast
    db.add_post("Alice", "Hello world")
    db.add_post("Bob", "I like cats")
    
    # Reads are slow
    feed = db.get_feed(["Alice", "Bob"])
    print(f"Feed: {feed}")

# optimal.py
import time

# ==========================================
# ✅ OPTIMAL: PUSH MODEL (Fan-out on Write)
# ==========================================
# SCENARIO: "Celebrity" vs "Normal User".
#
# STRATEGY: 
# 1. Pre-compute the Feed. When Alice posts, push it to Bob's ready-made list.
# 2. Hybrid: 
#    - Normal users (Push): Push to friends' feeds.
#    - Celebrities (Pull): Don't push to 100M followers. Fetch their posts at read-time.

class FeedService:
    def __init__(self):
        self.user_feeds = {} # Map user_id -> List of posts (Pre-computed)
        self.celebrity_posts = {} # Map celeb_id -> List of posts
        
    def post_status(self, user_id, content, followers, is_celebrity=False):
        post = {"u": user_id, "c": content, "t": time.time()}
        
        if is_celebrity:
            # 🚀 CELEBRITY: Write once (Fast Write). Users Pull later.
            print(f"   🌟 [Celeb] Storing post for {user_id} in global cache.")
            if user_id not in self.celebrity_posts: self.celebrity_posts[user_id] = []
            self.celebrity_posts[user_id].append(post)
        else:
            # 🤵 NORMAL: Fan-out to all followers (Fast Read later).
            print(f"   📡 [Normal] Fan-out post to {len(followers)} feeds.")
            for f_id in followers:
                if f_id not in self.user_feeds: self.user_feeds[f_id] = []
                self.user_feeds[f_id].insert(0, post) # Prepend
                
    def get_feed(self, user_id, followed_celebs):
        # 1. Get pre-computed feed (O(1))
        feed = self.user_feeds.get(user_id, [])[:]
        
        # 2. Merge Celebrity posts (Pull)
        for celeb in followed_celebs:
            if celeb in self.celebrity_posts:
                feed.extend(self.celebrity_posts[celeb])
                
        # 3. Sort merged result
        feed.sort(key=lambda x: x["t"], reverse=True)
        return feed

if __name__ == "__main__":
    service = FeedService()
    
    # Normal User Post
    service.post_status("Alice", "My lunch", followers=["Bob", "Charlie"])
    
    # Celebrity Post (Justin Bieber)
    service.post_status("Bieber", "Baby baby", followers=["Bob"] * 1000000, is_celebrity=True)
    
    # Bob reads feed
    print("\n📬 Bob's Feed:")
    feed = service.get_feed("Bob", followed_celebs=["Bieber"])
    for p in feed:
        print(f"   - {p['u']}: {p['c']}")
        
    print("\n🏆 Insight: Fan-out for normal users avoids read-latency.")
    print("   Pull for celebrities avoids 'Thundering Herd' writes.")

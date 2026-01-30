
import pytest
import sys
import os
import importlib.util

# Helper to load modules from arbitrary paths
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# Load Interview Questions Modules
q4_chat = load_module("chat", "05_interview_prep/Q4_ChatSystem/optimal.py")
q6_news = load_module("news", "05_interview_prep/Q6_NewsFeed/optimal.py")
q9_rank = load_module("rank", "05_interview_prep/Q9_GamingLeaderboard/optimal.py")
q10_tix = load_module("tix", "05_interview_prep/Q10_Ticketmaster/optimal.py")
q15_pay = load_module("pay", "05_interview_prep/Q15_PaymentSystem/optimal.py")

class TestInterviewLogic:
    """
    Customized Logic Tests for Interview Prep Questions.
    Verifies the ALGORITHMS work, not just that the file runs.
    """

    def test_q6_news_feed_fanout(self):
        """Verify Push Model (Fan-out) puts posts in friends' feeds."""
        service = q6_news.FeedService()
        # Alice posts, Bob follows Alice
        service.post_status("Alice", "Hello", followers=["Bob"])
        
        # Check Bob's feed
        feed = service.get_feed("Bob", followed_celebs=[])
        assert len(feed) == 1
        assert feed[0]['c'] == "Hello"
        
        # Check Charlie (not a follower)
        feed_c = service.get_feed("Charlie", [])
        assert len(feed_c) == 0

    def test_q9_leaderboard_ordering(self):
        """Verify Redis ZSet logic sorts correctly."""
        redis = q9_rank.MockRedisZSet()
        redis.zadd("P1", 10)
        redis.zadd("P2", 30)
        redis.zadd("P3", 20)
        
        # Top 2 should be P2(30), P3(20)
        top = redis.zrevrange(2)
        assert top[0][0] == "P2"
        assert top[1][0] == "P3"

    def test_q10_ticketmaster_locking(self):
        """Verify DB Lock prevents overselling."""
        db = q10_tix.SafeSeatDB()
        db.seats = 1
        
        # We manually call book() sequentially to test logic. 
        # Threading tests are nondeterministic, so we test the LOCK logic via state.
        
        # 1. Success
        db.book("Alice")
        assert db.seats == 0
        
        # 2. Fail
        db.book("Bob")
        assert db.seats == 0
        
    def test_q15_payment_idempotency(self):
        """Verify same key doesn't charge twice."""
        bank = q15_pay.IdempotentBank()
        bank.balance = 100
        key = "uuid-123"
        
        # Charge 1
        bank.charge(10, key)
        assert bank.balance == 90
        
        # Charge 2 (Same Key) -> Should be ignored
        bank.charge(10, key)
        assert bank.balance == 90 # Still 90
        
        # Charge 3 (New Key)
        bank.charge(10, "uuid-456")
        assert bank.balance == 80

    def test_q4_chat_offline_delivery(self):
        """Verify offline messages are stored and forwarded."""
        user = q4_chat.UserConnection("Bob") 
        user.online = False # Offline
        
        user.send("Msg 1")
        assert len(user.inbox) == 1
        
        user.connect() # Should sync
        assert user.online == True
        assert len(user.inbox) == 0 # Flushed

# design_chat.py
import queue
import time
import threading

# ==========================================
# 💬 SYSTEM DESIGN: CHAT APP (WhatsApp)
# ==========================================
# CHALLENGES:
# 1. Real-time delivery (WebSockets).
# 2. Offline support (Store-and-Forward).
# 3. Ordered delivery (Sequence IDs).
# 4. Scale (1M users -> 100k active connections per server).

class UserConnection:
    def __init__(self, user_id):
        self.user_id = user_id
        self.online = False
        self.inbox = [] # Offline storage
        
    def send(self, msg):
        if self.online:
            print(f"   📡 [WebSocket] Push to {self.user_id}: '{msg}'")
        else:
            print(f"   💾 [DB] User offline. Storing for {self.user_id}: '{msg}'")
            self.inbox.append(msg)
            
    def connect(self):
        self.online = True
        print(f"   🟢 {self.user_id} connected.")
        if self.inbox:
            print(f"   📨 [Sync] Delivering pending messages to {self.user_id}: {self.inbox}")
            self.inbox = []

def run_simulation():
    print("--- 💬 Chat System Simulation ---")
    alice = UserConnection("Alice")
    bob = UserConnection("Bob") # Offline
    
    # 1. Real-time
    alice.connect()
    alice.send("Hello Bob anyone there?") # Bob offline
    
    # 2. Store and Forward
    bob.connect() # Should receive sync
    
    # 3. Bi-directional
    bob.send("Hey Alice! I'm here now.")
    
    print("\n🏆 Scale Tip: Use **Redis Pub/Sub** to sync messages between multiple WebSocket Servers.")
    print("   🏢 Real World: **WhatsApp** uses Erlang/FreeBSD for mass connections. **Discord** uses Elixir.")

if __name__ == "__main__":
    run_simulation()

# 01_notification_service.py
import queue
import time

# ==========================================
# 📢 NOTIFICATION SYSTEM (Pub/Sub)
# ==========================================
# SCENARIO: You need to send an Alert to: iOS, Android, Email, SMS.
# Sending sequentially takes forever.
# Solution: Fan-out Queues.

class NotificationExchange:
    def __init__(self):
        self.queues = {
            "email": queue.Queue(),
            "sms": queue.Queue(),
            "push": queue.Queue()
        }
        
    def publish(self, msg):
        print(f"📢 [Publisher] Fan-out event: '{msg}'")
        for q_name, q in self.queues.items():
            q.put(msg)
            print(f"   -> Enqueued to {q_name}")

class Consumer:
    def __init__(self, type):
        self.type = type
        
    def process(self, exchange):
        q = exchange.queues[self.type]
        while not q.empty():
            msg = q.get()
            print(f"✅ [{self.type.upper()} Worker] Sending: {msg}")

if __name__ == "__main__":
    exchange = NotificationExchange()
    exchange.publish("User 123 Registered")
    
    # Workers process in parallel (simulated here)
    print("\n--- Processing ---")
    Consumer("email").process(exchange)
    Consumer("sms").process(exchange)
    Consumer("push").process(exchange)

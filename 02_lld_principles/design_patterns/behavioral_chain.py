# behavioral_chain.py
from abc import ABC, abstractmethod

# ==========================================
# ⛓️ CHAIN OF RESPONSIBILITY (Middleware)
# ==========================================
# SCENARIO: An HTTP Request must pass through:
# 1. Auth Check (Is user logged in?)
# 2. Rate Limit (Too many requests?)
# 3. Logging (Record request)
# 4. The actual Handler.
#
# If step 1 fails, STOP. Do not proceed to 2.

class Handler(ABC):
    def __init__(self):
        self.next_handler = None
        
    def set_next(self, handler):
        self.next_handler = handler
        return handler # Return next for chaining
        
    @abstractmethod
    def handle(self, request):
        if self.next_handler:
            return self.next_handler.handle(request)
        return True

class AuthMiddleware(Handler):
    def handle(self, request):
        if request.get("token") != "secret":
            print("   ⛔ [Auth] 401 Unauthorized")
            return False
        print("   ✅ [Auth] Passed")
        return super().handle(request)

class RateLimitMiddleware(Handler):
    def handle(self, request):
        if request.get("calls", 0) > 5:
            print("   ⛔ [RateLimit] 429 Too Many Requests")
            return False
        print("   ✅ [RateLimit] Passed")
        return super().handle(request)

class LoggingMiddleware(Handler):
    def handle(self, request):
        print(f"   📝 [Log] Request: {request}")
        return super().handle(request)

if __name__ == "__main__":
    print("--- ⛓️ Chain of Responsibility (Middleware) ---")
    
    # Build Pipeline
    # Auth -> RateLimit -> Log
    auth = AuthMiddleware()
    auth.set_next(RateLimitMiddleware()).set_next(LoggingMiddleware())
    
    print("\n1. Valid Request:")
    auth.handle({"token": "secret", "calls": 1, "body": "Hello"})
    
    print("\n2. Invalid Token:")
    auth.handle({"token": "hack", "calls": 1})
    
    print("\n3. Rate Limited:")
    auth.handle({"token": "secret", "calls": 10})
    
    print("\n🏆 Application: ExpressJS/FastAPI Middleware, LangChain Pipelines.")

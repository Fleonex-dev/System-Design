# ==========================================
# ✅ OPTIMAL SOLUTION (Base62 + Distributed ID)
# ==========================================
# CONCEPTS:
# 1. Distributed ID: Snowflake ID or DB Auto-Increment (with ranges).
# 2. Base62: Convert unique Integer ID -> Short String.
#    (0-9, a-z, A-Z) = 62 chars.
#    62^6 = ~56 Billion combinations. Plenty for 6 chars.

class Base62Encoder:
    CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    def encode(self, num):
        if num == 0: return self.CHARS[0]
        res = []
        while num > 0:
            res.append(self.CHARS[num % 62])
            num //= 62
        return "".join(reversed(res))

    def decode(self, s):
        num = 0
        for char in s:
            num = num * 62 + self.CHARS.index(char)
        return num

class TinyURLGood:
    def __init__(self):
        self.encoder = Base62Encoder()
        self.id_counter = 100000000 # Starting at a high number for 5-char length
        self.db = {}
        
    def shorten(self, url):
        # 1. Get Unique Integer ID (In prod, ask the DB or Snowflake ID generator)
        uid = self.id_counter
        self.id_counter += 1
        
        # 2. Convert to Base62
        short_link = self.encoder.encode(uid)
        
        # 3. Save
        self.db[short_link] = url
        return short_link

if __name__ == "__main__":
    print("✅ Shortening URLs deterministically...")
    app = TinyURLGood()
    
    code = app.shorten("https://google.com")
    print(f"✅ Short Code: {code}")
    print(f"✅ ID Behind scenes: {app.encoder.decode(code)}")

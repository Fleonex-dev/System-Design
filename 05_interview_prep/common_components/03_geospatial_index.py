# 03_geospatial_index.py
import random

# ==========================================
# 📍 GEOSPATIAL INDEXING (QuadTree / Geohash)
# ==========================================
# SCENARIO: Uber "Find Drivers Near Me".
# NAIVE: "SELECT * FROM drivers WHERE sqrt((x-x2)^2...) < 5" -> Full Table Scan. Slow!
# OPTIMIZED: Divide world into boxes (QuadTree). Only check drivers in MY box.

class Driver:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class QuadTree:
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary # (x, y, w, h)
        self.capacity = capacity
        self.drivers = []
        self.divided = False
        
    def insert(self, driver):
        # 1. Check boundary
        x, y, w, h = self.boundary
        if not (x <= driver.x < x + w and y <= driver.y < y + h):
            return False 
            
        # 2. Add if room
        if len(self.drivers) < self.capacity:
            self.drivers.append(driver)
            return True
            
        # 3. Split if full
        if not self.divided:
            self.subdivide()
            
        # 4. Pass do children
        return (self.nw.insert(driver) or self.ne.insert(driver) or
                self.sw.insert(driver) or self.se.insert(driver))

    def subdivide(self):
        x, y, w, h = self.boundary
        half_w = w / 2
        half_h = h / 2
        
        self.nw = QuadTree((x, y, half_w, half_h))
        self.ne = QuadTree((x + half_w, y, half_w, half_h))
        self.sw = QuadTree((x, y + half_h, half_w, half_h))
        self.se = QuadTree((x + half_w, y + half_h, half_w, half_h))
        self.divided = True

    def query(self, search_boundary):
        found = []
        x, y, w, h = self.boundary
        sx, sy, sw, sh = search_boundary
        
        # Intersection check
        if (sx > x + w or sx + sw < x or sy > y + h or sy + sh < y):
            return found # No intersection
            
        for d in self.drivers:
            if (sx <= d.x < sx + sw and sy <= d.y < sy + sh):
                found.append(d)
                
        if self.divided:
            found.extend(self.nw.query(search_boundary))
            found.extend(self.ne.query(search_boundary))
            found.extend(self.sw.query(search_boundary))
            found.extend(self.se.query(search_boundary))
            
        return found

if __name__ == "__main__":
    print("--- 📍 QuadTree Simulation (Uber) ---")
    # World is 100x100
    qt = QuadTree((0, 0, 100, 100))
    
    # 1. Simulate 100 Drivers randomly
    for i in range(100):
        d = Driver(i, random.uniform(0, 100), random.uniform(0, 100))
        qt.insert(d)
        
    # 2. User at (50, 50) looks for drivers within 10 units
    print("🔍 User at (50,50) searching radius 10 box...")
    search_box = (40, 40, 20, 20)
    nearby = qt.query(search_box)
    
    print(f"✅ Found {len(nearby)} drivers instantly.")
    for d in nearby[:3]:
        print(f"   🚕 Driver {d.id} at ({d.x:.1f}, {d.y:.1f})")
        
    print("\n🏆 Insight: We filtered 100 drivers without iterating all 100.")
    print("   🏢 Real World: **Uber** uses Google S2 (Space-Filling Curves). **Yelp** uses Geohash.")
    print("   **Postgres PostGIS** uses R-Trees (similar concept).")

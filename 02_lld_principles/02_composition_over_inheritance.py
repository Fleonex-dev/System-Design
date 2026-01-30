# 02_composition_over_inheritance.py

# ==========================================
# 🧩 COMPOSITION OVER INHERITANCE
# ==========================================
# SCENARIO: Designing a 'Robot'.
#
# ❌ INHERITANCE (Rigid):
# class Robot
# class FlyingRobot(Robot)
# class SwimmingRobot(Robot)
# class FlyingSwimmingRobot(FlyingRobot, SwimmingRobot) -> DIAMOND PROBLEM! 💥
#
# ✅ COMPOSITION (Flexible):
# Robot HAS-A MovementStrategy.
# Robot HAS-A Tool.
# We "Compose" the robot from parts.

# --- Components ---
class Engine:
    def move(self): print("   💨 Engine: Vroom!")

class Wings:
    def move(self): print("   🦅 Wings: Flap flap!")

class Propeller:
    def move(self): print("   🚤 Propeller: Splish splash!")

# --- The Host ---
class Robot:
    def __init__(self, name):
        self.name = name
        self.movement_parts = []
        
    def add_part(self, part):
        self.movement_parts.append(part)
        
    def move(self):
        print(f"🤖 [{self.name}] Moving:")
        for part in self.movement_parts:
            part.move()

if __name__ == "__main__":
    print("--- 🧩 Composition Demo ---")
    
    # Build a Drone (Flies)
    drone = Robot("Drone")
    drone.add_part(Wings())
    drone.move()
    
    # Build a Seaplane (Flies + Swims)
    # With Inheritance, this is hard (Multiple Inheritance hell).
    # With Composition, it's 2 lines.
    seaplane = Robot("Seaplane")
    seaplane.add_part(Wings())
    seaplane.add_part(Propeller())
    seaplane.move()
    
    print("\n🏆 Rule: Favor 'HAS-A' relationships over 'IS-A'.")

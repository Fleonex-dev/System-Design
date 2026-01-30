# ==========================================
# 💀 THE CHALLENGE: FIX THIS "GOD OBJECT"
# ==========================================
# SCENARIO: 
# This Class does EVERYTHING.
# 1. It calculates math (Business Logic).
# 2. It formats strings (Presentation Layer).
# 3. It prints to console (I/O).
# 4. It has hardcoded "English" and "Spanish" support.
#
# PROBLEMS:
# - Violates SRP (Single Responsibility).
# - Violates OCP (Open Closed Principle). To add "French", you must modify the class.
# - Violates DIP. Tightly coupled to "print".
#
# GOAL:
# Refactor using:
# - STRATEGY Pattern for Languages (EnglishStrategy, SpanishStrategy).
# - OBSERVER Pattern for Output (PrintObserver, FileObserver).
# - Clean separation of concerns.

class GodCalculator:
    def __init__(self, lan="en"):
        self.lan = lan
        
    def calculate(self, a, b, op):
        res = 0
        if op == "add":
            res = a + b
        elif op == "sub":
            res = a - b
            
        # FORMATTING LOGIC
        msg = ""
        if self.lan == "en":
            msg = f" The result is {res}"
        elif self.lan == "es":
            msg = f" El resultado es {res}"
            
        # I/O LOGIC
        print(f"💀 [CONSOLE]: {msg}")
        with open("log.txt", "a") as f:
            f.write(msg + "\n")

    def change_lan(self, lan):
        self.lan = lan

if __name__ == "__main__":
    calc = GodCalculator()
    calc.calculate(5, 3, "add")
    
    # Needs to change language?
    calc.change_lan("es")
    calc.calculate(10, 2, "sub")

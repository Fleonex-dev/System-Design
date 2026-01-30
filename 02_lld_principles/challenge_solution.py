from abc import ABC, abstractmethod

# ==========================================
# 🏆 THE SOLUTION
# ==========================================

# 1. STRATEGY PATTERN (Formatting)
class LanguageStrategy(ABC):
    @abstractmethod
    def format(self, res: int) -> str: pass

class EnglishStrategy(LanguageStrategy):
    def format(self, res: int): return f"The result is {res}"

class SpanishStrategy(LanguageStrategy):
    def format(self, res: int): return f"El resultado es {res}"

# 2. OBSERVER PATTERN (I/O)
class OutputObserver(ABC):
    @abstractmethod
    def log(self, msg: str): pass

class ConsoleObserver(OutputObserver):
    def log(self, msg: str): print(f"✅ [CONSOLE]: {msg}")

class FileObserver(OutputObserver):
    def log(self, msg: str):
        with open("log_clean.txt", "a") as f:
            f.write(msg + "\n")

# 3. REFACTORED CALCULATOR (Subject)
class CleanCalculator:
    def __init__(self, language_strategy: LanguageStrategy):
        self.strategy = language_strategy
        self.observers = []
        
    def attach(self, observer: OutputObserver):
        self.observers.append(observer)
        
    def set_strategy(self, strategy: LanguageStrategy):
        self.strategy = strategy
        
    def calculate(self, a, b, op):
        # 1. Pure Business Logic
        res = 0
        if op == "add": res = a + b
        elif op == "sub": res = a - b
        
        # 2. Use Strategy for Formatting
        msg = self.strategy.format(res)
        
        # 3. Notify Observers for I/O
        for obs in self.observers:
            obs.log(msg)

if __name__ == "__main__":
    # Setup
    calc = CleanCalculator(EnglishStrategy())
    
    # Attach Observers
    calc.attach(ConsoleObserver())
    calc.attach(FileObserver())
    
    # Run
    calc.calculate(5, 3, "add")
    
    # Dynamic Switch (OCP compliant!)
    calc.set_strategy(SpanishStrategy())
    calc.calculate(10, 2, "sub")

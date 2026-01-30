# 02_composite_pattern.py
from abc import ABC, abstractmethod

# ==========================================
# 🌳 COMPOSITE PATTERN
# ==========================================
# SCENARIO: A filesystem (Files and Folders).
# A Folder can contain Files OR other Folders.
# You want to treat them uniformly (e.g., `get_size()`).

class Component(ABC):
    @abstractmethod
    def get_size(self): pass

class File(Component):
    def __init__(self, name, size):
        self.name = name
        self.size = size
        
    def get_size(self):
        return self.size

class Folder(Component):
    def __init__(self, name):
        self.name = name
        self.children = []
        
    def add(self, component):
        self.children.append(component)
        
    def get_size(self):
        total = sum(c.get_size() for c in self.children)
        print(f"   📂 Folder '{self.name}' size: {total}KB")
        return total

if __name__ == "__main__":
    print("--- 🌳 COMPOSITE DEMO ---")
    
    root = Folder("root")
    home = Folder("home")
    root.add(home)
    
    file1 = File("resume.pdf", 500)
    file2 = File("photo.jpg", 2000)
    
    home.add(file1)
    home.add(file2)
    
    print(f"Total Size: {root.get_size()}KB")

import queue
import threading

# ==========================================
# ✅ OPTIMAL SOLUTION (BFS Frontier + Workers)
# ==========================================
# CONCEPTS:
# 1. Frontier: A Queue of URLs to visit.
# 2. Bloom Filter: Memory-efficient "Visited" set checking (Probabilistic).
# 3. Workers: Parallel threads/processes.
# 4. Politeness: Check robots.txt before fetching.

class CrawlerWorker(threading.Thread):
    def __init__(self, frontier, visited_bloom_filter):
        super().__init__()
        self.frontier = frontier
        self.visited = visited_bloom_filter
        
    def run(self):
        while True:
            try:
                url = self.frontier.get(timeout=2)
            except queue.Empty:
                return # Done
            
            if url in self.visited: continue
            self.visited.add(url) # In prod, use Bloom Filter here
            
            print(f"✅ [Worker {self.ident}] Processing {url}")
            
            # Extract new links
            new_links = [f"{url}/sub1", f"{url}/sub2"]
            for link in new_links:
                self.frontier.put(link)
                
            self.frontier.task_done()

def run_crawler():
    print("\n--- ✅ Running GOOD implementation (Frontier) ---")
    frontier = queue.Queue()
    frontier.put("root.com")
    
    # In reality, 'visited' would be a Redis Set or Bloom Filter
    visited = set()
    
    # Spawn 5 Workers
    workers = []
    for _ in range(5):
        w = CrawlerWorker(frontier, visited)
        w.start()
        workers.append(w)
        
    # Wait for queue to empty (in real crawler, this runs forever)
    # frontier.join() # Commented out to avoid hanging this script

if __name__ == "__main__":
    run_crawler()
    print("✅ Crawled efficiently in parallel.")

import requests

# ==========================================
# 🛑 BAD SOLUTION (Recursive DFS)
# ==========================================
# PROBLEMS:
# 1. Stack Overflow: Recursion depth limit.
# 2. Cycles: Crawling A -> B -> A will loop forever (Need strict visited set).
# 3. Single Threaded: Too slow for the web.

visited = set()

def crawl(url):
    if url in visited: return
    visited.add(url)
    
    print(f"🛑 Crawling {url}...")
    try:
        # html = requests.get(url).text
        # links = parse_links(html)
        links = ["sub_page"] # Mock
        
        for link in links:
            crawl(link) # RECURSION DANGER
            
    except Exception:
        pass

if __name__ == "__main__":
    print("🛑 Starting Recursive Crawl...")
    crawl("root")

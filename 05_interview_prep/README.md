# 💼 System Design Interview Prep

> "Scale is not a feature, it's a requirement."

This module contains **complete interview solutions** for the most common System Design questions asked at FAANG/AI labs.
Each question follows a standard interview flow:
1. **Clarify**: Define the scope.
2. **Design (HLD)**: Draw the boxes.
3. **Deep Dive (LLD)**: Write the code / algorithms.
4. **Scale**: Handle millions of users.

## 📚 Question Bank

### [Q1: Distributed Rate Limiter](./Q1_RateLimiter)
* **Goal**: Limit users to 10 requests/sec.
* **Core Concept**: Sliding Window Log vs Token Bucket. Redis Lua Scripts.

### [Q2: URL Shortener (TinyURL)](./Q2_URLShortener)
* **Goal**: Shorten 1B URLs per month.
* **Core Concept**: Base62 Encoding, ID Generation, Redirect 301 vs 302.

### [Q3: Web Crawler](./Q3_WebCrawler)
* **Goal**: Crawl the entire web (10B pages).
* **Core Concept**: Frontier Queue, DNS Resolution, Politeness, Bloom Filters.

(More coming soon...)

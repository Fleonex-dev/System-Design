# Contributing to System Design Masterclass

## 🚀 The Golden Rule: Branch & Merge
We follow a strict **Feature Branch Workflow** to ensure stability.
The `main` branch should always be deployable (and passing tests).

### 1. Create a Branch
Never work on `main` directly.
```bash
git checkout -b feat/my-new-feature
# or
git checkout -b fix/concurrency-bug
```

### 2. Verify Locally
Before pushing, ensure you haven't broken anything.
```bash
make test
```

### 3. Push & Open Pull Request
```bash
git push origin feat/my-new-feature
```
- Go to GitHub and open a **Pull Request (PR)**.
- **Wait for CI**: Our GitHub Actions pipeline will automatically run.
- **Green Check?** ✅ -> Safe to Merge.
- **Red X?** ❌ -> Fix code, commit, and push again (PR updates automatically).

### 4. Code Style
- **Python**: We use `pylint` and `pytest`.
- **Naming**: Snake_case for functions/files (`01_rate_limiter.py`).
- **Simulations**: Scripts should demonstrate a concept and exit gracefully.

---
*Happy Coding!*

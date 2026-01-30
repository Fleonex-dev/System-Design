# ☁️ System Design: Google Drive / Dropbox

## 🧠 The Concept
Syncing large files across devices efficiently.

## 🛑 The Challenge (Naive Approach)
*   **Method**: Uploading the entire file on every save.
*   **Problem**:
    1.  **Bandwidth**: Changing 1 byte in a 1GB file requires re-uploading 1GB.
    2.  **Latency**: Slow sync times.

## ✅ The Solution (Optimal)
*   **Strategy**: **Block-Level Deduplication** (Rsync algo).
    1.  Split file into 4MB chunks.
    2.  Hash each chunk (SHA-256).
    3.  Only upload chunks that have changed (or exist in the cloud already).
*   **Result**: 99% bandwidth saving on minor edits.

# 📺 System Design: YouTube / Netflix

## 🧠 The Concept
Streaming high-quality video to millions of users with varying internet speeds.

## 🛑 The Challenge (Naive Approach)
*   **Method**: Sending a single MP4 file via HTTP Range requests.
*   **Problem**:
    1.  **Buffering**: A 4K video will freeze on a 3G connection.
    2.  **Latency**: User has to wait for huge download.

## ✅ The Solution (Optimal)
*   **Strategy**: **Adaptive Bitrate Streaming (ABS)**.
*   **Protocols**: **HLS** (Apple) or **DASH**.
*   **Mechanism**:
    1.  Transcode video into chunks (2-10 seconds) at multiple resolutions (360p, 720p, 1080p).
    2.  Client player detects bandwidth and selects the best chunk every few seconds.
    3.  **CDN**: Content is served from edge locations.

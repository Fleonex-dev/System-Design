# bad.py
import time

# ==========================================
# 🛑 BAD: SINGLE VIDEO FILE
# ==========================================
# SCENARIO: User has slow internet (3G). Video is 4K.
# NAIVE: Send the 4K MP4 file.
#
# PROBLEM:
# 1. Buffering hell.
# 2. Wasted bandwidth (User stops watching after 10s, but we downloaded 100MB).

class VideoServer:
    def stream(self, video_file):
        print(f"   🐢 Streaming full file '{video_file}' (1GB)...")
        # Simulating buffering
        for i in range(5):
            print("   ⏳ Buffering...", end="\r")
            time.sleep(0.5)
        print("\n   ❌ Playback stalled. User quit.")

if __name__ == "__main__":
    server = VideoServer()
    server.stream("movie_4k.mp4")

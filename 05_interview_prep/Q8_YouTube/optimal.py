# optimal.py
import time

# ==========================================
# ✅ OPTIMAL: ADAPTIVE BITRATE (HLS/DASH)
# ==========================================
# STRATEGY:
# 1. Transcode video into chunks (144p, 360p, 720p, 1080p).
# 2. Client detects bandwidth.
# 3. Client requests the best chunk it can handle.

class AdaptiveStreamer:
    def __init__(self):
        self.chunks = {
            "1080p": "HD Chunk (High)",
            "360p": "SD Chunk (Med)",
            "144p": "Mobile Chunk (Low)"
        }
        
    def stream_segment(self, bandwidth_mbps):
        # Adaptive Logic
        quality = "144p"
        if bandwidth_mbps > 5: quality = "1080p"
        elif bandwidth_mbps > 1: quality = "360p"
        
        data = self.chunks[quality]
        print(f"   📡 [Bandwidth {bandwidth_mbps} Mbps] Fetching {quality} segment -> Playing Smoothly.")
        
if __name__ == "__main__":
    player = AdaptiveStreamer()
    
    print("--- 📺 YouTube Adaptive Streaming ---")
    
    # Scene 1: Good Internet
    player.stream_segment(bandwidth_mbps=10)
    
    # Scene 2: Driving under tunnel (Network drop)
    print("   ⚠️ Network Drop detected!")
    player.stream_segment(bandwidth_mbps=0.5)
    
    # Scene 3: Back to normal
    player.stream_segment(bandwidth_mbps=8)
    
    print("\n🏆 Insight: Never send one big file. Split it up.")
    print("   **Netflix** and **YouTube** use CDNs to store these chunks close to you.")

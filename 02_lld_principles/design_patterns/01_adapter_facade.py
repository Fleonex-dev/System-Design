# 01_adapter_facade.py

# ==========================================
# 🔌 ADAPTER PATTERN
# ==========================================
# SCENARIO: You have a Legacy Payment API (XML) but your new system speaks JSON.
# Instead of rewriting the Legacy system, you wrap it.

class LegacyXMLPayment:
    def make_payment_xml(self, xml_data):
        print(f"   [Legacy] Processing XML: {xml_data}")

class ModernJSONPayment:
    def pay_json(self, json_data):
        pass

class PaymentAdapter(ModernJSONPayment):
    def __init__(self, legacy_service):
        self.legacy = legacy_service
        
    def pay_json(self, json_data):
        # Translate JSON -> XML
        xml = f"<amount>{json_data['amount']}</amount>"
        print(f"   [Adapter] Translated JSON {json_data} -> XML {xml}")
        self.legacy.make_payment_xml(xml)

# ==========================================
# 🏛️ FACADE PATTERN
# ==========================================
# SCENARIO: A complex subsystem (Video Converter) has Audio, Video, Codec, Bitrate classes.
# The user just wants "convert(mp4)".
# The Facade hides the complexity.

class AudioMixer:
    def fix(self): print("   [Audio] Mixing...")

class VideoTranscoder:
    def encode(self): print("   [Video] Transcoding 4K...")

class SubtitleManager:
    def sync(self): print("   [Subs] Syncing...")

class VideoConverterFacade:
    def __init__(self):
        self.audio = AudioMixer()
        self.video = VideoTranscoder()
        self.subs = SubtitleManager()
        
    def convert(self, file):
        print(f"🎬 [Facade] Converting {file}...")
        self.audio.fix()
        self.video.encode()
        self.subs.sync()
        print("✅ Done.")

if __name__ == "__main__":
    print("--- 🔌 ADAPTER DEMO ---")
    legacy = LegacyXMLPayment()
    adapter = PaymentAdapter(legacy)
    adapter.pay_json({"amount": 100})
    
    print("\n--- 🏛️ FACADE DEMO ---")
    converter = VideoConverterFacade()
    converter.convert("movie.mkv")

# 05_grpc_vs_rest.py
import json
import struct
import sys

# ==========================================
# 📡 PROTOCOLS: gRPC (Protobuf) vs REST (JSON)
# ==========================================
# SCENARIO: Sending "{id: 123, price: 99.99, active: true}"
# JSON: Human readable string. Heavy.
# Protobuf: Binary. Compact. Fast.

def simulate_json():
    # REST / JSON
    data = {"id": 123, "price": 99.99, "active": True}
    json_bytes = json.dumps(data).encode('utf-8') # "{"id": 123...}"
    return json_bytes

def simulate_protobuf():
    # gRPC / Protobuf
    # Schema: int32(1), float(2), bool(3)
    # We use python 'struct' to mimic binary packing
    # Field 1 (id): val 123
    # Field 2 (price): val 99.99
    # Field 3 (active): val 1
    
    # Pack: Interger (4 bytes) + Float (4 bytes) + Bool (1 byte)
    # This is a simplification; real ProtoBuf uses varints and field tags.
    proto_bytes = struct.pack('if?', 123, 99.99, True)
    return proto_bytes

if __name__ == "__main__":
    print("--- 📦 Payload Comparison ---")
    
    # JSON
    j = simulate_json()
    print(f"JSON Payload: '{j.decode()}'")
    print(f"JSON Size:    {len(j)} bytes")
    
    # Proto
    p = simulate_protobuf()
    print(f"Proto Sim:    {p}")
    print(f"Proto Size:   {len(p)} bytes")
    
    diff = len(j) - len(p)
    print(f"\n📉 Savings: {diff} bytes per request.")
    print("   At 1 Billion reqs/day = 10 TB bandwidth saved.")

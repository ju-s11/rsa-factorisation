#!/usr/bin/env python3
"""
Analyze the decrypted output
"""
import base64

# Your decrypted hex
hex_data = "63287608c4b7ae1cf046d1eddbcd4c84f498cca79687e9290e511d726e16e376b1478a6c604b78540ab7094dfefac24abc867ee601bd4292459225d21accdb70c7454c8741685294"

# Convert hex to bytes
decrypted_bytes = bytes.fromhex(hex_data)

print(f"Total length: {len(decrypted_bytes)} bytes")
print("\n=== Trying different interpretations ===")

# 1. Try as ASCII with different offsets
print("\n1. ASCII (different starting points):")
for i in range(0, min(20, len(decrypted_bytes))):
    try:
        ascii_text = decrypted_bytes[i:].decode('ascii', errors='ignore')
        # Look for flag patterns
        if 'FLAG' in ascii_text or 'flag' in ascii_text or '{' in ascii_text:
            print(f"  Starting at byte {i}: {ascii_text[:100]}")
    except:
        pass

# 2. Try UTF-8
print("\n2. UTF-8:")
try:
    utf8_text = decrypted_bytes.decode('utf-8', errors='ignore')
    print(f"  {utf8_text[:200]}")
except:
    print("  Not valid UTF-8")

# 3. Look for PKCS#1 padding pattern (common in RSA)
print("\n3. Check for PKCS#1 padding:")
# PKCS#1 v1.5 padding starts with 00 02 ... 00
if decrypted_bytes[:2] == b'\x00\x02':
    print("  Found PKCS#1 padding (00 02)")
    # Find the 00 separator
    try:
        zero_pos = decrypted_bytes.index(b'\x00', 2)
        message = decrypted_bytes[zero_pos+1:]
        print(f"  Message starts at position {zero_pos+1}")
        print(f"  Message (hex): {message.hex()}")
        print(f"  Message (ASCII): {message.decode('ascii', errors='ignore')}")
    except:
        print("  Could not find message separator")

# 4. Try to reverse the bytes
print("\n4. Reversed bytes:")
reversed_bytes = decrypted_bytes[::-1]
try:
    reversed_text = reversed_bytes.decode('ascii', errors='ignore')
    print(f"  {reversed_text[:200]}")
except:
    print("  Not readable")

# 5. Try to extract printable characters only
print("\n5. Printable ASCII only:")
printable = ''.join(chr(b) for b in decrypted_bytes if 32 <= b < 127)
print(f"  {printable[:200]}")

# 6. Check if it's base64 encoded data
print("\n6. Check for embedded base64:")
for i in range(0, len(decrypted_bytes)-4):
    chunk = decrypted_bytes[i:i+100]
    try:
        # Try to decode as base64
        decoded = base64.b64decode(chunk)
        # If it decodes and contains printable text
        decoded_str = decoded.decode('ascii', errors='ignore')
        if len(decoded_str) > 10 and any(c.isalpha() for c in decoded_str):
            print(f"  Found base64 at position {i}: {decoded_str[:100]}")
    except:
        pass

# 7. Try XOR with common values
print("\n7. Simple XOR patterns:")
for xor_val in [0x20, 0x55, 0xAA, 0xFF]:
    xored = bytes(b ^ xor_val for b in decrypted_bytes)
    try:
        text = xored.decode('ascii', errors='ignore')
        if 'flag' in text.lower() or 'FLAG' in text:
            print(f"  XOR with 0x{xor_val:02x}: {text[:100]}")
    except:
        pass
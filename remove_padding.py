#!/usr/bin/env python3
"""
Remove PKCS#1 v1.5 padding to reveal the flag
"""
import base64

# Your decrypted hex (from 05_decrypt.py output)
hex_data = "02159b07401a5dfe9326a7a8dc5471ed8d3f93a65616db0916aecf1332550254fed5416522689e476b02141dee60522186e06065ffd8f0007570326c36446e6149685a6778410a"

# Convert to bytes
padded_data = bytes.fromhex(hex_data)

print(f"Total length: {len(padded_data)} bytes")
print(f"First few bytes: {padded_data[:20].hex()}")

# PKCS#1 v1.5 padding format:
# 00 02 [random non-zero bytes] 00 [message]

if padded_data[0] == 0x00 and padded_data[1] == 0x02:
    print("\nDetected PKCS#1 v1.5 padding")
    print("Format: 00 02 [padding] 00 [message]")
    
    # Find the 00 separator after padding
    try:
        # Start looking from position 2 (after 00 02)
        separator_pos = -1
        for i in range(2, len(padded_data)):
            if padded_data[i] == 0x00:
                separator_pos = i
                break
        
        if separator_pos != -1:
            print(f"Found separator at position {separator_pos}")
            
            # Extract the message (everything after the 00 separator)
            message = padded_data[separator_pos + 1:]
            
            print(f"\nExtracted message ({len(message)} bytes):")
            print(f"Hex: {message.hex()}")
            
            # Try to decode as text
            try:
                flag = message.decode('utf-8')
                print(f"\nFLAG FOUND: {flag}")
                
                # Save to file
                with open('flag.txt', 'w') as f:
                    f.write(flag)
                print("Flag saved to flag.txt")
                
            except UnicodeDecodeError:
                print("\nMessage is not UTF-8 text")
                print("Trying ASCII...")
                flag = message.decode('ascii', errors='ignore')
                if flag.strip():
                    print(f"ASCII: {flag}")
                else:
                    print("Not plain ASCII either")
                    
                    # Try different interpretations
                    print("\nOther interpretations:")
                    
                    # 1. As integer
                    from Crypto.Util.number import bytes_to_long
                    num = bytes_to_long(message)
                    print(f"As integer: {num}")
                    
                    # 2. Try base64 encoding of the message
                    b64_msg = base64.b64encode(message).decode()
                    print(f"Base64 encoded: {b64_msg}")
                    
                    # 3. Try to find flag pattern
                    ascii_only = ''.join(chr(b) for b in message if 32 <= b < 127)
                    print(f"Printable ASCII only: {ascii_only}")
                    
                    # Look for common flag formats
                    import re
                    patterns = [r'FLAG\{[^}]*\}', r'flag\{[^}]*\}', r'[A-Z0-9_]{10,}']
                    for pattern in patterns:
                        matches = re.findall(pattern, ascii_only)
                        if matches:
                            print(f"Pattern match '{pattern}': {matches}")
            
        else:
            print("ERROR: Could not find 00 separator in PKCS#1 padding")
            
    except Exception as e:
        print(f"Error: {e}")
        
else:
    print("\nNot PKCS#1 v1.5 format")
    print(f"First bytes: {padded_data[:2].hex()}")
    print("Expected: 00 02")

# Alternative: Try to brute-force find the flag
print("\n" + "="*50)
print("Brute-force search for flag in data:")

# Convert entire padded data to ASCII (ignore errors)
all_ascii = padded_data.decode('ascii', errors='ignore')
print(f"All ASCII characters: {all_ascii}")

# Look for common flag indicators
indicators = ['FLAG', 'flag', '{', '}']
for indicator in indicators:
    if indicator in all_ascii:
        pos = all_ascii.find(indicator)
        print(f"Found '{indicator}' at position {pos}")
        
        # Extract around it
        start = max(0, pos - 5)
        end = min(len(all_ascii), pos + 30)
        print(f"Context: ...{all_ascii[start:end]}...")
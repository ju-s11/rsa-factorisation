from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse
import base64

# Your values
n = 188198812920607963838697239461650439807163563379417382700763356422988859715234665485319060606504743045317388011303396716199692321205734031879550656996221305168759307650257059
e = 65537
p = 398075086424064937397125500550386491199064362342526708406385189575946388957261768583317
q = 472772146107435302536223071973048224632914695302097116459852171130520711256363590397527

# Verify
if p * q != n:
    print("ERROR: p*q != n")
    exit()

print("p and q verified ✓")

# Ciphertext
def fix_padding(b64):
    return b64 + '=' * (4 - len(b64) % 4) if len(b64) % 4 else b64

ciphertext_b64 = "e8oQDihsmkvjT3sZe+EE8lwNvBEsFegYF6+OOFOiR6gMtMZxxba/bIgLUD8pV3yEf0gOOfHuB5bC3vQmo7bE4PcIKfpFGZBA"
c = bytes_to_long(base64.b64decode(fix_padding(ciphertext_b64)))

# Compute private key and decrypt
phi = (p-1)*(q-1)
d = inverse(e, phi)
m = pow(c, d, n)

# CRITICAL: Convert to bytes with the correct length
# RSA output should be exactly (n.bit_length() + 7) // 8 bytes
byte_length = (n.bit_length() + 7) // 8
decrypted_bytes = long_to_bytes(m, byte_length)  # Force specific length

print(f"\nDecrypted bytes length: {len(decrypted_bytes)}")
print(f"Expected length for {n.bit_length()}-bit n: {byte_length} bytes")
print(f"First 10 bytes (hex): {decrypted_bytes[:10].hex()}")

# Check for PKCS#1 padding
if len(decrypted_bytes) >= 2:
    if decrypted_bytes[0] == 0x00 and decrypted_bytes[1] == 0x02:
        print("\nFound PKCS#1 v1.5 padding (00 02)")
        
        # Find the 00 separator
        try:
            separator = decrypted_bytes.index(b'\x00', 2)
            message = decrypted_bytes[separator+1:]
            print(f"Message starts at byte {separator+1}")
            print(f"Message length: {len(message)} bytes")
            
            # Try to decode
            try:
                flag = message.decode('utf-8')
                print(f"\nFLAG: {flag}")
                
                # Also check if it's the Root-me format
                if flag.startswith('FLAG'):
                    print("This is likely the correct flag!")
                elif 'flag' in flag.lower():
                    print(f"Found flag-like text: {flag}")
                    
            except UnicodeDecodeError:
                print(f"\nMessage hex: {message.hex()}")
                print(f"Message ASCII: {message.decode('ascii', errors='ignore')}")
                
                # Try to interpret as text
                ascii_text = ''.join(chr(b) for b in message if 32 <= b < 127)
                if ascii_text:
                    print(f"Printable ASCII: {ascii_text}")
                    
        except ValueError:
            print("ERROR: Could not find 00 separator in PKCS#1 padding")
            print(f"Full data (hex): {decrypted_bytes.hex()}")
            
    elif decrypted_bytes[0] == 0x02:  # Missing leading 00
        print("\nFound 02 (missing leading 00)")
        print("Adding leading 00 and trying again...")
        
        # Add the missing 00
        fixed_bytes = b'\x00' + decrypted_bytes
        print(f"Fixed bytes start: {fixed_bytes[:10].hex()}")
        
        if len(fixed_bytes) >= 2 and fixed_bytes[1] == 0x02:
            try:
                separator = fixed_bytes.index(b'\x00', 2)
                message = fixed_bytes[separator+1:]
                
                try:
                    flag = message.decode('utf-8')
                    print(f"\nFLAG (fixed): {flag}")
                except:
                    print(f"Message hex: {message.hex()}")
                    print(f"Message ASCII: {message.decode('ascii', errors='ignore')}")
            except:
                print("Still couldn't find separator")
                
    else:
        print(f"\nUnknown format. First bytes: {decrypted_bytes[:4].hex()}")
        
        # Try to extract any text anyway
        all_text = decrypted_bytes.decode('ascii', errors='ignore')
        print(f"All ASCII: {all_text}")
        
        # Look for flag patterns
        import re
        patterns = [r'FLAG\{[^}]*\}', r'flag\{[^}]*\}', r'[A-Z0-9_]{10,}']
        for pattern in patterns:
            matches = re.findall(pattern, all_text)
            if matches:
                print(f"Pattern '{pattern}' found: {matches}")

print("\n" + "="*50)
print("Alternative: Try manual extraction")

# Based on your earlier output that showed "c(vFL)QrnvGl`KxTMJ~BE%pELAhR"
# The "FL" suggests the flag might be there

# Your original hex from earlier attempt:
old_hex = "63287608c4b7ae1cf046d1eddbcd4c84f498cca79687e9290e511d726e16e376b1478a6c604b78540ab7094dfefac24abc867ee601bd4292459225d21accdb70c7454c8741685294"
old_bytes = bytes.fromhex(old_hex)

print(f"\nOriginal decryption had {len(old_bytes)} bytes")
print("Searching for 'FLAG' pattern...")

# Convert to string, looking for flag
for i in range(len(old_bytes)):
    # Check for F L A G sequence
    if (i + 3 < len(old_bytes) and 
        old_bytes[i] == ord('F') and 
        old_bytes[i+1] == ord('L') and 
        old_bytes[i+2] == ord('A') and 
        old_bytes[i+3] == ord('G')):
        
        print(f"Found 'FLAG' at position {i}")
        # Extract potential flag
        potential = old_bytes[i:].decode('ascii', errors='ignore')
        print(f"Potential: {potential[:50]}")
        break

# If not found, try lowercase
for i in range(len(old_bytes)):
    if (i + 3 < len(old_bytes) and 
        old_bytes[i] == ord('f') and 
        old_bytes[i+1] == ord('l') and 
        old_bytes[i+2] == ord('a') and 
        old_bytes[i+3] == ord('g')):
        
        print(f"Found 'flag' at position {i}")
        potential = old_bytes[i:].decode('ascii', errors='ignore')
        print(f"Potential: {potential[:50]}")
        break

print("\nTrying all printable ASCII from original:")
ascii_chars = ''.join(chr(b) for b in old_bytes if 32 <= b < 127)
print(ascii_chars)
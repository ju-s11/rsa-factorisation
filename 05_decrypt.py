#!/usr/bin/env python3
"""
Decrypt the ciphertext using found private key
"""
from Crypto.Util.number import long_to_bytes, bytes_to_long
import base64

def add_padding(base64_string):
    """Add padding to base64 string if needed"""
    padding_needed = 4 - len(base64_string) % 4
    if padding_needed != 4:
        base64_string += '=' * padding_needed
    return base64_string

def decrypt_ciphertext():
    """Decrypt the ciphertext with available keys"""
    print("\n=== Decrypting Ciphertext ===")
    
    # Read ciphertext (FIXED PADDING)
    ciphertext_b64 = "e8oQDihsmkvjT3sZe+EE8lwNvBEsFegYF6+OOFOiR6gMtMZxxba/bIgLUD8pV3yEf0gOOfHuB5bC3vQmo7bE4PcIKfpFGZBA"
    
    # Fix padding
    ciphertext_b64 = add_padding(ciphertext_b64)
    
    try:
        ciphertext_bytes = base64.b64decode(ciphertext_b64)
        c = bytes_to_long(ciphertext_bytes)
        print(f"Ciphertext decoded successfully")
        print(f"Ciphertext as integer: {c}")
    except Exception as e:
        print(f"Error decoding ciphertext: {e}")
        print(f"Base64 string (with padding): {ciphertext_b64}")
        return
    
    # Try to read factors from file
    try:
        with open('factors.txt', 'r') as f:
            lines = f.readlines()
            p = int(lines[0].split('=')[1].strip())
            q = int(lines[1].split('=')[1].strip())
        
        print("Using factors from factorization...")
    except:
        try:
            with open('wiener_results.txt', 'r') as f:
                lines = f.readlines()
                d = int(lines[0].split('=')[1].strip())
                p = int(lines[1].split('=')[1].strip())
                q = int(lines[2].split('=')[1].strip())
            
            print("Using results from Wiener attack...")
        except:
            print("No private key found!")
            print("Run factorization or Wiener attack first")
            return
    
    # Compute private key
    with open('key_parameters.txt', 'r') as f:
        e_line = f.readlines()[1]
        e = int(e_line.split('=')[1].strip())
    
    n = p * q
    phi = (p-1)*(q-1)
    
    # Compute d if not from Wiener attack
    if 'd' not in locals():
        from Crypto.Util.number import inverse
        d = inverse(e, phi)
    
    print(f"\nPrivate key components:")
    print(f"  p = {p}")
    print(f"  q = {q}")
    print(f"  n = {n}")
    print(f"  e = {e}")
    print(f"  d = {d}")
    print(f"  phi = {phi}")
    
    # Decrypt
    print("\nDecrypting...")
    m = pow(c, d, n)
    
    # Convert to bytes
    try:
        flag = long_to_bytes(m).decode('utf-8')
        print(f"\nFLAG FOUND: {flag}")
        
        with open('flag.txt', 'w') as f:
            f.write(flag)
        print("Flag saved to flag.txt")
        
    except UnicodeDecodeError:
        print(f"\nDecrypted integer: {m}")
        print("Raw bytes (hex):", long_to_bytes(m).hex())
        
        # Try different encodings
        bytes_data = long_to_bytes(m)
        print("\nTrying different interpretations:")
        print(f"  As ASCII: {bytes_data.decode('ascii', errors='ignore')}")
        print(f"  As hex: {bytes_data.hex()}")
        print(f"  As base64: {base64.b64encode(bytes_data).decode()}")

if __name__ == "__main__":
    decrypt_ciphertext()
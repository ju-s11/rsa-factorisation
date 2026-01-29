#!/usr/bin/env python3
"""
Extract RSA parameters from PEM public key
"""
from Crypto.PublicKey import RSA

def extract_key_info(pem_file='pubkey.pem'):
    """Extract n, e from PEM file"""
    print("=== Extracting RSA Parameters ===")
    
    # Read the PEM file
    with open(pem_file, 'r') as f:
        key_data = f.read()
    
    # Import RSA key
    key = RSA.import_key(key_data)
    
    print(f"Modulus (n): {key.n}")
    print(f"Public exponent (e): {key.e}")
    print(f"Bit length of n: {key.n.bit_length()} bits")
    print(f"Bit length of e: {key.e.bit_length()} bits")
    
    # Save to file for later use
    with open('key_parameters.txt', 'w') as f:
        f.write(f"n = {key.n}\n")
        f.write(f"e = {key.e}\n")
        f.write(f"n_bits = {key.n.bit_length()}\n")
        f.write(f"e_bits = {key.e.bit_length()}\n")
    
    return key.n, key.e

if __name__ == "__main__":
    n, e = extract_key_info()
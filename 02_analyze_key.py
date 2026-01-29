#!/usr/bin/env python3
"""
Analyze RSA key for potential vulnerabilities
"""
from Crypto.Util.number import isPrime
import math

def analyze_key(n, e):
    """Analyze RSA key for weaknesses"""
    print("\n=== Analyzing Key for Vulnerabilities ===")
    
    # 1. Check n size
    n_bits = n.bit_length()
    print(f"1. Modulus size: {n_bits} bits")
    
    if n_bits < 256:
        print("   WARNING: n < 256 bits - easily factorable!")
    elif n_bits < 512:
        print("   WARNING: n < 512 bits - likely factorable")
    elif n_bits < 1024:
        print("   MODERATE: n < 1024 bits - might be factorable")
    else:
        print("   STRONG: n >= 1024 bits - hard to factor")
    
    # 2. Check if e is large (suggests small d - Wiener attack)
    print(f"\n2. Public exponent analysis:")
    print(f"   e = {e}")
    print(f"   e/n approx: {e/n:.10f}")
    
    if e > n:
        print("   WARNING: e > n - This suggests d might be small!")
    elif e > n * 0.9:
        print("   WARNING: e is very large - d might be small (Wiener attack possible)")
    elif e == 65537:
        print("   Common secure value: e = 65537")
    elif e == 3:
        print("   WARNING: Small e = 3 - vulnerable to broadcast attacks")
    
    # 3. Check for obvious weaknesses
    print(f"\n3. Basic checks:")
    
    # Check if n is even
    if n % 2 == 0:
        print("   CRITICAL: n is even - not a valid RSA modulus!")
    
    # Check if n is prime (should be composite)
    if isPrime(n):
        print("   CRITICAL: n is prime - not a valid RSA modulus!")
    else:
        print("   OK: n is composite (good)")
    
    # 4. Wiener attack condition check
    print(f"\n4. Wiener attack possibility:")
    wiener_limit = pow(n, 0.25) / 3
    print(f"   Wiener attack works if d < {wiener_limit:.2f}")
    print(f"   (d would have < {math.log2(wiener_limit):.1f} bits)")

if __name__ == "__main__":
    # Read n and e from previous step
    with open('key_parameters.txt', 'r') as f:
        lines = f.readlines()
        n = int(lines[0].split('=')[1].strip())
        e = int(lines[1].split('=')[1].strip())
    
    analyze_key(n, e)
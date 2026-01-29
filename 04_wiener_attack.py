#!/usr/bin/env python3
"""
Wiener attack for small private exponent d
Based on continued fractions
"""
from Crypto.Util.number import inverse, long_to_bytes
import math

def continued_fraction(e, n):
    """Generate continued fraction expansion of e/n"""
    cf = []
    while n:
        q = e // n
        cf.append(q)
        e, n = n, e - q * n
    return cf

def convergents(cf):
    """Generate convergents from continued fraction"""
    convs = []
    for i in range(len(cf)):
        if i == 0:
            num, den = cf[0], 1
        elif i == 1:
            num, den = cf[0]*cf[1] + 1, cf[1]
        else:
            num = cf[i]*convs[-1][0] + convs[-2][0]
            den = cf[i]*convs[-1][1] + convs[-2][1]
        convs.append((num, den))
    return convs

def wiener_attack(e, n):
    """Perform Wiener attack to find small d"""
    print("\n=== Attempting Wiener Attack ===")
    
    cf = continued_fraction(e, n)
    convs = convergents(cf)
    
    print(f"Generated {len(convs)} convergents")
    
    for k, d in convs:
        if k == 0:
            continue
            
        # Check if this k/d could be the correct one
        phi = (e*d - 1)//k
        
        # Try to recover p and q from phi
        b = n - phi + 1
        discriminant = b*b - 4*n
        
        if discriminant >= 0:
            root = math.isqrt(discriminant)
            if root*root == discriminant:  # Perfect square
                p = (b + root) // 2
                q = (b - root) // 2
                
                if p*q == n:
                    print(f"Found possible solution!")
                    print(f"   k = {k}")
                    print(f"   d = {d}")
                    print(f"   p = {p}")
                    print(f"   q = {q}")
                    return d, p, q
    
    print("Wiener attack failed - d might not be small enough")
    return None, None, None

if __name__ == "__main__":
    # Read parameters
    with open('key_parameters.txt', 'r') as f:
        lines = f.readlines()
        n = int(lines[0].split('=')[1].strip())
        e = int(lines[1].split('=')[1].strip())
    
    # Try Wiener attack
    d, p, q = wiener_attack(e, n)
    
    if d:
        with open('wiener_results.txt', 'w') as f:
            f.write(f"d = {d}\n")
            f.write(f"p = {p}\n")
            f.write(f"q = {q}\n")
        print("\nWiener results saved to wiener_results.txt")
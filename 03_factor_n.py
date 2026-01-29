#!/usr/bin/env python3
"""
Attempt to factor the modulus n - QUICK VERSION
"""
import sympy
import requests
import time

def quick_factor_check(n):
    """Check if n is small enough to factor quickly"""
    print("\n=== Quick Factor Check ===")
    n_bits = n.bit_length()
    
    if n_bits < 100:
        print(f"n has {n_bits} bits - should factor instantly")
        return True
    elif n_bits < 256:
        print(f"n has {n_bits} bits - might factor in seconds")
        return True
    elif n_bits < 512:
        print(f"n has {n_bits} bits - could take minutes/hours")
        print("Skipping factorization, trying Wiener attack instead")
        return False
    else:
        print(f"n has {n_bits} bits - too large to factor")
        print("This is NOT a factorization challenge!")
        return False

def try_small_factors(n):
    """Try to find small factors quickly"""
    print("\n=== Checking for small factors ===")
    
    # Try small primes
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
                   53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    for p in small_primes:
        if n % p == 0:
            q = n // p
            print(f"Found small factor: {p}")
            print(f"p = {p}")
            print(f"q = {q}")
            return p, q
    
    print("No small factors found")
    return None

def check_factordb(n):
    """Check FactorDB online"""
    print("\n=== Checking FactorDB (online) ===")
    
    try:
        url = f"http://factordb.com/api?query={n}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data['status']}")
            
            if data['status'] == 'FF':  # Fully Factored
                factors = data['factors']
                print(f"Found {len(factors)} factors")
                
                if len(factors) == 2:
                    p = int(factors[0][0])
                    q = int(factors[1][0])
                    print(f"p = {p}")
                    print(f"q = {q}")
                    return p, q
    except:
        print("Could not connect to FactorDB")
    
    return None

if __name__ == "__main__":
    # Read n from file
    with open('key_parameters.txt', 'r') as f:
        n_line = f.readline()
        n = int(n_line.split('=')[1].strip())
    
    # Quick check
    if not quick_factor_check(n):
        print("\nSkipping intensive factorization.")
        print("Run 04_wiener_attack.py instead.")
        exit(0)
    
    # Try quick methods
    factors = try_small_factors(n)
    
    if not factors:
        factors = check_factordb(n)
    
    # Only try sympy if n is small
    if not factors and n.bit_length() < 128:
        print("\n=== Trying sympy (last resort) ===")
        try:
            start = time.time()
            factors = sympy.factorint(n)
            print(f"Time: {time.time() - start:.2f}s")
            
            if len(factors) == 2:
                p, q = list(factors.keys())
                print(f"p = {p}")
                print(f"q = {q}")
                factors = (p, q)
        except:
            print("Sympy failed or timed out")
    
    # Save if found
    if factors:
        p, q = factors
        with open('factors.txt', 'w') as f:
            f.write(f"p = {p}\n")
            f.write(f"q = {q}\n")
        print("\nFactors saved to factors.txt")
    else:
        print("\nNo factors found.")
        print("Proceed to Wiener attack: python 04_wiener_attack.py")
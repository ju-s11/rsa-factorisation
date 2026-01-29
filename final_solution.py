# final_solution.py
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse
import base64

# RSA parameters from challenge
n = 188198812920607963838697239461650439807163563379417382700763356422988859715234665485319060606504743045317388011303396716199692321205734031879550656996221305168759307650257059
e = 65537

# Factors from FactorDB
p = 398075086424064937397125500550386491199064362342526708406385189575946388957261768583317
q = 472772146107435302536223071973048224632914695302097116459852171130520711256363590397527

# Ciphertext
ciphertext_b64 = "e8oQDihsmkvjT3sZe+EE8lwNvBEsFegYF6+OOFOiR6gMtMZxxba/bIgLUD8pV3yEf0gOOfHuB5bC3vQmo7bE4PcIKfpFGZBA"

# Decrypt
ciphertext_b64 += '=' * (4 - len(ciphertext_b64) % 4)  # Fix padding
c = bytes_to_long(base64.b64decode(ciphertext_b64))

phi = (p-1)*(q-1)
d = inverse(e, phi)
m = pow(c, d, n)

# Convert to bytes with correct length
byte_length = (n.bit_length() + 7) // 8
decrypted = long_to_bytes(m, byte_length)

# Remove PKCS#1 v1.5 padding
if decrypted[0:2] == b'\x00\x02':
    separator = decrypted.index(b'\x00', 2)
    flag = decrypted[separator+1:].decode('utf-8')
    print(f"Flag: {flag}")
else:
    print("Unexpected format")
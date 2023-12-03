'''
https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf
The round constant word array, Rcon[i], contains the values given by
[x**i-1,{00},{00},{00}], with x**i-1 being powers of x (x is denoted as {02})
in the field GF(28), as discussed in Sec. 4.2 (note that i starts at 1, not 0)
'''

# these are the expected round constants up to round 29
# note that rijndael variants with larger block sizes than aes can use
# up 30 full rounds of key expansion and as a result require 29 round constants
expected_rc = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36,
    0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6,
    0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5
]

# aes 128's key schedule requires the first 10 round constants
rc_for_aes_128 = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36
]

# aes 192's key schedule requires the first 8 round constants
rc_for_aes_192 = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80
]

# aes 192's key schedule requires the first 7 round constants
rc_for_aes_256 = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40
]

def multiply_in_gf2(a, b, mod):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:
            a ^= mod
        b >>= 1
    return result

# rc[0] = x**0 = 2**0 = 1
rc = [1]

for i in range(1, 29):
    # rc[i] = 2 * rc[i-1] mod P
    rc.append(multiply_in_gf2(2, rc[i-1], 0x11B))

for i in range(len(expected_rc)):
    assert(expected_rc[i] == rc[i])

print("aes round contants ~ method 1")
for i in range(len(rc)):
    print(f"[{i + 1:02}] = {rc[i]:02x}")

# alternate method i found online
# https://math.stackexchange.com/a/4345415

def compute_rc(round):
    rc = 0xCB
    for i in range(0, round + 1):
        rc <<= 1
        if rc > 0xFF:
            rc ^= 0x11B
    return rc

print("aes round contants ~ method 2")
for i in range(30):
    print(f"[{i:02}] = {compute_rc(i):02x}")


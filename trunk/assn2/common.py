import random
import string

FMT_HEADER = "!i"
HEADER_SIZE = 4

CHUNK_SIZE = 8

# This needs to be a string of length CHUNK_SIZE
IV = "ranDoM45"

def random_string(n):
    return ''.join(random.choice(string.ascii_letters + string.digits)
                   for i in range(n))

def pad(s):
    # Pads the string with 0s in case it's not divisible by CHUNK_SIZE
    padding = (CHUNK_SIZE - (len(s) % CHUNK_SIZE)) % CHUNK_SIZE
    return s + '0'*padding

def chunkify(s):
    s = pad(s)
    return [s[i:i+CHUNK_SIZE] for i in xrange(0, len(s), CHUNK_SIZE)]

def str_xor(s1, s2):
    # Based on code found here:
    # http://stackoverflow.com/questions/2612720/how-to-do-bitwise-exclusive-
    # or-of-two-strings-in-python
    return ''.join(chr(ord(c1)^ord(c2)) for c1,c2 in zip(s1, s2))

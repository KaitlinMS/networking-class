import random
import string

CHUNK_SIZE = 8

def random_string(n):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(n))

#KEY_LEN = 64
#KEY = random_string(KEY_LEN)
IV = "ranDoM45"

def chunkify(s):
    return [list(s[CHUNK_SIZE*i:CHUNK_SIZE*(i+1)]) for i in range(len(s)/CHUNK_SIZE)]

def str_xor(s1, s2):
    return ''.join(chr(ord(s)^ord(c)) for s,c in zip(s1, s2))

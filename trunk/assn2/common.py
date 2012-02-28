"""
common.py
A collection of a few common constants and functions 
used by both the client and server.

************************************************************
SFWR ENG 4C03 - Assignment 2
Authors:
Cameron Sapp		   - 0768086
Kaitlin Smith		   - 0645771
Manivanna Thevathasan  - 0754015
************************************************************
"""

FMT_HEADER = "!i"
HEADER_SIZE = 4

CHUNK_SIZE = 8

# These need to be strings of length >= CHUNK_SIZE
IV = "ranDoM45"
KEY = "l0oKak3y"

def pad(s):
    """
    Pads the string with 0s in case it's not divisible by CHUNK_SIZE
    """
    padding = (CHUNK_SIZE - (len(s) % CHUNK_SIZE)) % CHUNK_SIZE
    return s + '0'*padding

def chunkify(s):
    """
    Breaks a string into a list of chunks of length CHUNK_SIZE
    """
    s = pad(s)
    return [s[i:i+CHUNK_SIZE] for i in xrange(0, len(s), CHUNK_SIZE)]

def str_xor(s1, s2):
    # Based on code found here:
    # http://stackoverflow.com/questions/2612720/how-to-do-bitwise-exclusive-
    # or-of-two-strings-in-python
    return ''.join(chr(ord(c1)^ord(c2)) for c1,c2 in zip(s1, s2))


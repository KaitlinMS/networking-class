import socket
import random
import string

import common

class Client(object):

    def dh(self, msg):
        return msg

    def encrypt(self, msg):
        chunks = common.chunkify(msg)
        ciphertext = [common.str_xor(common.IV, chunks[0])]
        for i in range(1, len(chunks)):
            ci = self.dh(common.str_xor(chunks[i], ciphertext[i-1]))
            ciphertext.append(ci)
        return ''.join(ciphertext)

    def run(self, host, port):
        msg = raw_input("Enter a message: ")
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, port))
        conn.sendall(self.encrypt(msg))
        conn.close()

if __name__ == "__main__":
    import sys
    host, port = sys.argv[1], int(sys.argv[2])
    Client().run(host, port)


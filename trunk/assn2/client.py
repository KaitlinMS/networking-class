import struct
import socket

import common

class Client(object):

    def block_cipher_encrypt(self, chunk):
        return chunk

    def pad(self, msg):
        cs = common.CHUNK_SIZE
        padding = (cs - (len(msg) % cs)) % cs
        return msg + '0'*padding

    def encrypt(self, msg):
        chunks = common.chunkify(self.pad(msg))
        ciphertext = [common.str_xor(common.IV, chunks[0])]
        for i in range(1, len(chunks)):
            ci = self.block_cipher_encrypt(
                    common.str_xor(chunks[i], ciphertext[i-1]))
            ciphertext.append(ci)
        return ''.join(ciphertext)

    def run(self, host, port):
        msg = raw_input("Enter a message: ")
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, port))
        header = struct.pack(common.FMT_HEADER, len(msg))
        conn.sendall(header + self.encrypt(msg))
        conn.close()

if __name__ == "__main__":
    import sys
    host, port = sys.argv[1], int(sys.argv[2])
    Client().run(host, port)


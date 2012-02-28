"""
Usage:
python client.py <host> <port>

************************************************************
SFWR ENG 4C03 - Assignment 2
Authors:
Cameron Sapp		   - 0768086
Kaitlin Smith		   - 0645771
Manivanna Thevathasan  - 0754015
************************************************************
"""

import time
import struct
import socket

import common

class Client(object):

    def encrypt_chunk(self, chunk):
        return common.str_xor(chunk, common.KEY)

    def encrypt(self, msg):
        chunks = common.chunkify(msg)
        ciphertext = [self.encrypt_chunk(common.str_xor(common.IV, chunks[0]))]
        for i in range(1, len(chunks)):
            ci = self.encrypt_chunk(common.str_xor(chunks[i], ciphertext[i-1]))
            ciphertext.append(ci)
        return ''.join(ciphertext)

    def get_user_msg(self):
        msg = ''
        while not msg:
            msg = raw_input("Enter a message: ")
        return msg

    def connect(self):
        sleep_time = 5
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                conn.connect((host, port))
                return conn
            except socket.error, e:
                print "Could not connect. Retrying in %d seconds" % \
                        sleep_time
                time.sleep(sleep_time)


    def run(self, host, port):
        msg = self.get_user_msg()
        header = struct.pack(common.FMT_HEADER, len(msg))

        conn = self.connect()
        conn.sendall(header + self.encrypt(msg))
        conn.close()


if __name__ == "__main__":
    import sys
    host, port = sys.argv[1], int(sys.argv[2])
    Client().run(host, port)


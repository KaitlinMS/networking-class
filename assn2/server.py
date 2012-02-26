import socket

import common

class Server(object):

    def __init__(self, port):
        self.port = port
        self.host = ''

    def dh(self, msg):
        return msg

    def decrypt(self, data):
        chunks = common.chunkify(data)
        plaintext = [common.str_xor(common.IV, self.dh(chunks[0]))]
        for i in range(1, len(chunks)):
            pi = common.str_xor(chunks[i-1], self.dh(chunks[i]))
            plaintext.append(pi)
        return ''.join(plaintext)

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(1)
        print "Server listening..."
        conn, addr = s.accept()
        while 1:
            data = conn.recv(1024)
            if not data:
                break
            print self.decrypt(data)
        conn.close()

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1])
    Server(port).run()

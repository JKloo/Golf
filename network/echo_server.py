# Echo server program
import socket
import threading

from settings import HOST, PORT, PACKET_SIZE

class EchoServer(threading.Thread):
    def __init__(self):
        ''' '''
        threading.Thread.__init__(self)
        self.daemon = True
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((HOST, PORT))
        self.s.listen(1)
        self.CONN, self.ADDR = self.s.accept()
        print 'Connected by', self.ADDR
        self.start()

    def run(self):
        ''' '''
        while True:
            data = self.CONN.recv(PACKET_SIZE)
            # if not data: break
            self.CONN.sendall(data)
        self.CONN.close()

ES = EchoServer()
while True:
    pass

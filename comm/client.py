import pickle
import socket

from config.settings import PACKET_SIZE, EXTERN_HOST, PORT, PROMPT, TIME_OUT

class Client(socket.socket):
    def __init__(self, host=EXTERN_HOST, port=PORT):
        self.ADDRESS = (host, port)
        socket.socket.__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connect(self.ADDRESS)

    def _send(self, s):
        self.sendall(s)

    def send(self, obj):
        s = pickle.dumps(obj)
        while True:
            try:
                self._send(s)
            except socket.error:
                pass
            else:
                break

    def _recv(self, sock):
        return sock.recv(PACKET_SIZE)

    def recv(self, sock):
        m = self._recv(sock)
        return pickle.loads(m)

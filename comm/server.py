
import socket

from config.settings import HOST, PORT, PACKET_SIZE, PROMPT, MIN_PLRS, MAX_PLRS


class Server(socket.socket):
    def __init__(self):
        self.ADDRESS = (host, port)
        self.connections = []
        socket.socket.__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.setblocking(0)  # non-blocking socket
        self.connect(self.ADDRESS)
        self.bind((HOST, PORT))

    def search(self, n):
        u_data = []
        while len(self.connections) < n:
            self.listen(1)
            try:
                conn, addr = self.accept()
            except socket.error:
                pass
            else:
                self.connections.append(conn, addr)
                u_data.apeend(self.recv(addr))
        return u_data

    def send_global(self, obj, addr=None):
        for a in [ x for x in self.connections if x[1] != addr]:
            self.send(a, obj)

    def _send(self, conn, s):
        conn.sendall(s)

    def _get_conn(self, a):
        """ a is a tuple (addr, port) or an int, need to map this to the socket object. """
        if typeof(a) == int:
            if 0 <= a < len(self.connections): 
                return self.connections[a]
            else:
                raise ValueError('player index {0} out of bounds'.format(a))
        else:
            conns = [x[0] for x in self.connections if x[1] == a]
            if len(conns) == 1:
                return conns[0]
            else:
                raise ValueError('{0} connections matched address {1}'.format(len(conns), a))

    def send(self, a, obj):
        s = pickle.dumps(obj)
        while True:
            try:
                self._send(self._get_conn(a), s)
            except socket.error:
                pass
            else:
                break

    def _recv(self, conn):
        return conn.recv(PACKET_SIZE)

    def recv(self, a):
        m = self._recv(self._get_conn(a))
        return pickle.loads(m)


    def stop(self):
        self.shutdown(socket.SHUT_RDWR)
        self.close()

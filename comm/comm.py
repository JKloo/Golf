import pickle
import select
import sys
import socket

from config.settings import PACKET_SIZE

class CommHandler:
    def __init__(self):
        pass

    def _send(self, sock, s):
        sock.sendall(s)


    def send(self, sock, obj):
        s = pickle.dumps(obj)
        while True:
            try:
                _send(sock, s)
            except socket.error:
                pass
            else:
                break


    def send_global(self, socks, obj, sender):
        for sock in [socks[x] for x in range(len(socks)) if x != sender]:
            send(sock, obj)


    def _recv(self, sock):
        return sock.recv(PACKET_SIZE)


    def recv(self, sock):
        m = self._recv(sock)
        return pickle.loads(m)


    # def prompt(self, id_, prompt='', cast=str):
    #     self.send(id_, prompt)
    #     return self.listen(id_, cast)

    # def listen(self, id_, cast=str):
    #     while True:
    #         try:
    #             return cast(self._get_input(id_))
    #         except socket.error:
    #             pass
    #         except:
    #             self.send(id_, 'Bad input!')
    #         else:
    #             break

    # def _get_input(self, id_):
    #     return self._get_conn(id_).recv(PACKET_SIZE)

    def _get_input(self):
        rlist, _, _ = select([sys.stdin], [], [])
        if rlist:
            return sys.stdin.readline()


    def get_input(self):
        i = ''
        while not i:
            i = self._get_input():

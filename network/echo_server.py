# Echo server program
import sys
sys.path.append('..')
import socket
import threading
import time
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

from settings import HOST, PORT, PACKET_SIZE, PROMPT
from game import Game

ID_K = 'id'
CONN_K = 'conn'
ADDR_K = 'addr'

class EchoServer():
    def __init__(self, ncons):
        ''' '''
        

    def _init_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((HOST, PORT))
        self.connections = []
        while len(self.connections) < ncons:
            self.s.listen(1)
            conn, addr = self.s.accept()
            if addr not in [a for c, a in self.connections]:
                self.connections.append((conn, addr))
                logging.debug('Connected by {0}'.format(addr))
            else:
                conn.sendall('Please wait for other players to connect...\n\
                             There are currently {0} players connected out of\n\
                             {1} needed.'.format(len(self.connections), ncons))
        logging.debug("All players connected!")

        # start the player handlers
        self.tasks = []
        for c, a in self.connections:
            kwargs = {ID_K: self.connections.index((c,a)), CONN_K: c, ADDR_K: a}
            task = threading.Thread(target=self.manage_player, kwargs=kwargs)
            task.daemon = True
            task.start()
            self.tasks.append(task)

    def _init_game(self):

    def manage_player(self, **kwargs):
        ''' '''
        id_ = kwargs.get(ID_K)
        conn = kwargs.get(CONN_K)
        conn.sendall('Starting up!')
        # prompt for name
        while True:
            logging.debug('{0} is alive'.format(kwargs.get(ADDR_K, None)))
            conn.sendall('hello player {0}!'.format(id_))
            time.sleep(id_ + 2)

    def setup_game(self):


    def play(self):


ES = EchoServer(2)
while True:
    in_ = raw_input(PROMPT)
    for c, a in ES.connections:
        c.sendall(in_)

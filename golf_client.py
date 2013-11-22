import sys
import socket
import threading
import time
import logging
from select import select
logging.basicConfig(level=logging.INFO, format='%(message)s')

from config.settings import PACKET_SIZE, EXTERN_HOST, PORT, PROMPT

TIME_OUT = 0.001


class GolfClient():
    ''' '''
    def __init__(self):
        ''' Initializes...everything. '''
        self.ADDRESS = (EXTERN_HOST, PORT)
        self.shutdown = False
        self.input = []

        # SOCK_DGRAM is the socket type to use for UDP sockets
        # AF_INET sets it to use UDP protocol
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #so the os doesn't complain
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #Find the server
        self.s.connect(self.ADDRESS)
        self.task_i = threading.Thread(target=self.get_input, name='I')
        self.task_i.daemon = True
        self.task_i.start()

        self.task_r = threading.Thread(target=self.receive, name='R')
        self.task_r.daemon = True
        self.task_r.start()

    def receive(self):
        logging.debug('starting receive thread')
        while not self.shutdown:
            msg = self.s.recv(PACKET_SIZE).strip()
            logging.debug('received message')
            logging.debug('waht?!?!?')
            if msg:
                self._handle_message(msg)
            else:
                self.shutdown = True
                break
        logging.debug('stopping receive thread')
        logging.info('game server closed')

    def _handle_message(self, msg):
        ''' '''
        print msg

    def main(self):
        ''' '''
        logging.debug('starting send thread')
        while not self.shutdown:
            if self.input:
                in_ = self.input.pop(0).strip()
                self.s.sendall(in_)
                logging.debug('sent message')
            time.sleep(0.1)
        logging.debug('stopping send thread')
        self.task_r.join()

    def get_input(self):
        ''' '''
        while not self.shutdown:
            in_ = ''
            rlist, wlist, _ = select([sys.stdin], [sys.stdout], [])
            if rlist:
                in_ = sys.stdin.readline()
                self.input.append(in_)
                logging.debug('got input: {0}'.format(in_))

    def send(self, msg):
        ''' '''
        self.s.sendall(msg, self.ADDRESS)

    def _main(self):
        ''' '''
        while not self.shutdown:
            in_ = ''
            rlist, wlist, _ = select([sys.stdin, self.s], [sys.stdout], [])
            if rlist:
                in_ = sys.stdin.readline()
                self.s.sendall(in_)


GC = GolfClient()
GC.main()

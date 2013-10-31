import socket
import threading
import time
import pickle
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

from settings import PACKET_SIZE, EXTERN_HOST, PORT
import user_settings
PROFILE = {'name': 'Jeff'}
PROMPT = '> '

class GolfClient(threading.Thread):
    ''' '''
    def __init__(self):
        '''
        Initializes...everything.  
        '''
        threading.Thread.__init__(self)
        self.ADDRESS = (EXTERN_HOST, PORT)
        self.daemon = True

        # SOCK_DGRAM is the socket type to use for UDP sockets
        # AF_INET sets it to use UDP protocol
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #so the os doesn't complain
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #Find the server
        self.s.connect(self.ADDRESS)
        # self.s.sendall(pickle.dumps(PROFILE))
        self.start()

    def run(self):
        '''
        implementation of the inherited run() method from the Thread class.  
        This is a separate thread from the main thread that is always receiving information
        '''
        logging.debug('starting receive thread')
        while True:
            msg = self.s.recv(PACKET_SIZE)
            logging.debug('received message')
            self._handle_message(msg)
        logging.debug('stopping receive thread')

    def _handle_message(self, msg):
        ''' '''
        print msg
   
    def run_send(self):
        ''' '''
        logging.debug('starting send thread')
        while True:
            in_ = self._get_input()
            logging.debug('got input: {0}'.format(in_))
            self.s.sendall(in_)
            logging.debug('sent message')
        logging.debug('stopping send thread')


    def _get_input(self):
        ''' '''
        in_ = str(raw_input(PROMPT))
        return in_

    def send(self, msg):
        ''' '''
        self.s.sendall(msg, self.ADDRESS)

GC = GolfClient()
GC.run_send()

import socket
import threading
import time
import golf
from game import Game

MAXPACKETSIZE = 1024
HOST = 'localhost'
PORT = 21567

class GolfServer(threading.Thread):
    ''' '''
    def __init__(self, nplayers):
        ''' '''
        threading.Thread.__init__(self)
        
        self.daemon = True
        self.TIMEOUT = 3.0
        self.stopreceivethread = True
        # SOCK_DGRAM is the socket type to use for UDP sockets
        # AF_INET sets it to use UDP protocol
        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # So that the OS doesn't complain
        self.SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #sets socket to be blocking along with a timeout, if can't be sent or received within 5 seconds then the timeout exception is raised
        self.SOCK.setblocking(1)
        self.SOCK.settimeout(self.TIMEOUT)
        listen_addr = (HOST, PORT)
        #Bind socket to address
        self.SOCK.bind(listen_addr)

        self.connections = [None for x in range(nplayers)]
        self.buffers = ['' for x in range(nplayers)]
        self.start()

    def run(self):
        '''
        Implementation of the inherited run() method from the Thread class.  
        This is a separate thread from the main thread that is always receiving information.

        '''
        while not self.stopreceivethread:
            msg, user = self.recvfrom(MAXPACKETSIZE)


    def cleanup(self):
        '''
        stops closes the socket and stops the receive thread
        '''
        self.stopreceivethread = True 
        self.ISCONNECTED = False
        time.sleep(0.01)
        self.SOCK.close()

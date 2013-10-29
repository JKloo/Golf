import socket
import threading
import time

from player import Player
from golf_server import MAXPACKETSIZE, HOST, PORT

class GolfClient(threading.Thread):
    ''' '''
    def __init__(self):
        '''
        Initializes...everything.  
        '''
        threading.Thread.__init__(self)
        self.HOST = HOST
        self.PORT = PORT
        self.ADDRESS = (self.HOST, self.PORT)
        self.stopreceivethread = True
        self.daemon = True
        self.TIMEOUT = 3.0

        # SOCK_DGRAM is the socket type to use for UDP sockets
        # AF_INET sets it to use UDP protocol
        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #so the os doesn't complain
        self.SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #sets socket to be blocking along with a timeout, if can't be sent to received within 5 seconds then the timeout exception is raised
        self.SOCK.setblocking(1)
        self.SOCK.settimeout(self.TIMEOUT)

        #Find the server
        self.SOCK.sendto("Hello!", self.ADDRESS)
        
        while not self.ISCONNECTED:
            try:
                self.SOCK.sendto(self.PAYLOAD,self.HOSTPORT)
                data, addr = self.SOCK.recvfrom(32)
                if data.strip() == 'hello client':
                    self.ISCONNECTED = True
                    self.stopreceivethread = False
                    break 
                time.sleep(0.3)
            except timeout:
                continue

    def send(self):
        '''
        sends whatever is in self.PAYLOAD. calls helpersend if it is large message.  Sends 'done' at the end of a packet
        '''
        
        if len(self.PAYLOAD) <= 0:
            return
        
        
        elif len(self.PAYLOAD)<=self.MAXPACKETSIZE:
            self.SOCK.sendto(self.PAYLOAD,self.HOSTPORT)
            self.SOCK.sendto('done',(self.HOST,self.PORT))
        else:
            self.SOCK.sendto(self.PAYLOAD[:self.MAXPACKETSIZE], self.HOSTPORT)
            self.helpersend(self.PAYLOAD[self.MAXPACKETSIZE:])

    def run(self):
        '''
        implementation of the inherited run() method from the Thread class.  
        This is a separate thread from the main thread that is always receiving information
        '''
        while not self.stopreceivethread:
            self.receive(self.MAXPACKETSIZE)
   
    def cleanup(self):
        '''
        stops closes the socket and stops the receive thread
        '''
        self.ISCONNECTED = False
        self.stopreceivethread = True 
        self.SOCK.close()

    


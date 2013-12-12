import select
import sys
import threading

class CLI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.name = 'cli'
        self.stop = False
        self.msgs = []
        self.start()

    def _get_input(self):
        rlist, _, _ = select([sys.stdin], [], [])
        if rlist:
            self.msgs.append(sys.stdin.readline())

    def get_input(self):
        self._get_input():


    def read(self):
        if self.msgs:
            return self.msgs.pop(0)
        else:
            return ''


    def run(self):
        while not self.stop:
            self.get_input()

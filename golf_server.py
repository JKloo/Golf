# Echo server program
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))
import socket
import threading
import time
import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

from config.settings import HOST, PORT, PACKET_SIZE, PROMPT, MIN_PLRS, MAX_PLRS
from config.commands import CHAT, NEXT, QUIT, DRAW, TOP, SWAP, HAND, LOOK
from cardgame.game import Game

ID_K = 'id'
CONN_K = 'conn'
ADDR_K = 'addr'

STATUS_K = 'status'
NO_CONN_S = 0
INIT_S = 1
READY_S = 2

NO_MSG = ''
POLL_TIME = 0.1
GLOBAL_CHAT = ['global', 'all']

class GolfServer():
    def __init__(self, n=0):
        ''' '''
        if not (MIN_PLRS <= n <= MAX_PLRS):
            while not (MIN_PLRS <= n <= MAX_PLRS):
                n = int(raw_input('How many players: ')) 
        self.nplayers = n
        self.tasks = []
        self.end_game = False
        self.game_start = False
        self.drawn = False
        self._init_game()
        self._init_server()
        # start the player handlers
        self._init_players()
        self.game_start = True



    def _init_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setblocking(0)  # non-blocking socket
        self.s.bind((HOST, PORT))
        self.connections = []


    def _init_players(self):
        while len(self.connections) < self.nplayers:
            self.s.listen(1)
            try:
                conn, addr = self.s.accept()
            except socket.error:
                pass
            else:
                self.connections.append((conn, addr))
                logging.debug('Connected by {0}'.format(addr))
                kwargs = {ID_K: self.connections.index((conn, addr))}
                task_p = threading.Thread(target=self._init_player, kwargs=kwargs)
                task_p.daemon = True
                task_p.start()
                self.tasks.append(task_p)
        logging.debug("All players connected!")


    def _init_player(self, **kwargs):
        # prompt for name
        id_ = kwargs.get(ID_K)
        name = self.prompt(id_, 'What is your name?')
        self.game.players[id_].name = name
        self.game.players[id_].seat = id_
        self.game.players[id_].other[CONN_K] = self._get_conn(id_)
        self.game.players[id_].other[STATUS_K] = INIT_S
        self.send(id_, 'Thanks {0}, you are player {1}'.format(name, id_))

        # prompt for cards to flip
        cards = []
        while len(cards) < 2:
            in_ = self.prompt(id_, 'Choose {0} cards to flip, separated by spaces: '.format(str(2-len(cards))))
            cs = in_.split()
            for c in cs:
                try:
                    c_int = int(c)
                except:
                    continue
                else:
                    cards.append(c_int) 

        for i in cards:
            self.game.players[id_].hand.cards[i].face_up()

        # start msg handling thread
        kwargs = {ID_K: id_}
        task = threading.Thread(target=self._manage_player, kwargs=kwargs)
        task.daemon = True
        task.start()
        self.tasks.append(task)
        # end thread


    def _init_game(self):
        '''  '''
        game = Game(self.nplayers)
        game.begin(6)
        self.active_card = game.deck.draw()[0]
        self.active_card.face_up()
        self.game = game


    def _manage_player(self, **kwargs):
        id_ = kwargs.get(ID_K)
        self.game.players[id_].other[STATUS_K] = READY_S
        self.send(id_, 'Starting up player {0}!'.format(id_))
        while not self.end_game:
            msg = self.listen(id_)
            logging.debug('received "{0}" from player {1}'.format(msg, id_))
            if msg in CHAT:
                self._manage_chat(id_)
            else:
                resp = NO_MSG
                if self.game.curr_plr.seat == id_:
                    resp = self._manage_active(id_, msg)
                else:
                    resp = self._manage_inactive(id_, msg)
                self.send(id_, resp)


    def _manage_chat(self, id_):
        ''' '''
        trg = self.prompt(id_, 'who? ')
        msg = self.prompt(id_, 'message: ')
        if trg in GLOBAL_CHAT:
            self.send_global(msg, id_)
        else:
            plrs = [p for p in self.game.players if p.name == trg]
            if plrs:
            # silently don't send if the player doesn't exist
                for p in plrs:
                    self.send(p.seat, msg)


    def _manage_active(self, id_, msg):
        ''' '''
        resp = NO_MSG
        plr = self.game.players[id_]
        if msg in DRAW and not self.drawn:
            self.drawn = True
            self.game.deck.discards.append(self.active_card)
            self.active_card = self.game.deck.draw()[0]
            self.active_card.face_up()
            resp = self.active_card.pretty_print()

        elif msg in TOP:
            resp = self.active_card.pretty_print()
            
        elif msg in SWAP:
            pos = self.prompt(id_, 'pos: ', int)
            self.active_card = plr.hand.swap(pos, self.active_card)
            self.active_card.face_up()
            self._manage_active(id_, NEXT[0])

        elif msg in HAND:
            resp = self._look_hand(plr)

        elif msg in LOOK:
            resp = self._look_board(self.game.players)

        elif msg in NEXT:
            self.game.next_player()
            self.end_game = self._detect_end_game()
            self.drawn = False

        logging.debug(resp)
        return resp


    def _manage_inactive(self, id_, msg):
        ''' '''
        invalid_cmds = [SWAP, NEXT, DRAW]
        flat_ics = [x for xs in invalid_cmds for x in xs]
        if msg in flat_ics:
            return 'Wait your turn!'
        else:
            return self._manage_active(id_, msg)


    def send(self, id_, msg):
        while True:
            try:
                self._send(id_, msg)
            except socket.error:
                pass
            else:
                break



    def _send(self, id_, msg):
        self._get_conn(id_).sendall(msg)


    def send_global(self, msg, sender):
        for i in range(len(self.connections)):
            if i != sender:
                self.send(i, msg)


    def prompt(self, id_, prompt='', cast=str):
        self.send(id_, prompt)
        return self.listen(id_, cast)


    def listen(self, id_, cast=str):
        while True:
            try:
                return cast(self._get_input(id_))
            except socket.error:
                pass
            except:
                self.send(id_, 'Bad input!')
            else:
                break

    def _get_input(self, id_):
        return self._get_conn(id_).recv(PACKET_SIZE)


    def _get_conn(self, id_):
        return self.connections[id_][0]


    def _look_hand(self, p):
        ''' '''
        resp = '{0}\'s hand:\n{1}'.format(p.name, p.hand.pretty_print())
        return resp


    def _look_board(self, players):
        ''' '''
        resp = ''
        for p in players:
            resp = resp + self._look_hand(p)
        return resp


    def _detect_end_game(self):
        ''' Detect the end of the game by checking if all cards are flipped. '''
        return not (False in [c.is_face_up() for c in self.game.curr_plr.hand.cards])


    def play(self):
        ''' '''
        while not self.end_game: time.sleep(0.1)
            # in_ = raw_input(PROMPT)
            # for i in range(len(ES.connections)):
            #     self.send(i, in_)


    def score(self):
        ''' Compute and display the scores. '''
        def _score(hand):
            ''' Compute a player's score. '''
            _s = 0
            for cs in hand.blocks:
                if hand.match(*cs):
                    _s -= 20
            for cs in hand.pairs:
                if not hand.match(*cs):
                    _s += sum([int(hand.cards[x]) for x in cs])
            return _s

        logging.info('Game over.')
        for p in self.game.players:
            p.hand.flip_all()
            p.score = _score(p.hand)
            self.send_global('{0}\'s hand:\n{1}'.format(p.name, self._look_hand(p)), None)
            logging.info('{0}\'s score: {1}'.format(p.name, p.score))
            self.send_global('{0}\'s score: {1}'.format(p.name, p.score), None)

        scores = [p.score for p in self.game.players]
        winner = self.game.players[scores.index(min(scores))]
        logging.info('The winner is: {0}!'.format(winner.name))
        self.send_global('The winner is: {0}!'.format(winner.name), None)
        # self.send_global('$@#$RQEGWBFHT^%#$@REQWDFRGTY$Y@$GQEA', None)
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
        for t in self.tasks:
            t.join()

ES = GolfServer()
ES.play()
ES.score()
for t in ES.tasks:
    print t.name, t.is_alive()

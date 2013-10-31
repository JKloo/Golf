# Echo server program
import sys
sys.path.append('..')
import socket
import threading
import time
import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

from settings import HOST, PORT, PACKET_SIZE, PROMPT, MIN_PLRS, MAX_PLRS
from commands import CHAT, NEXT, QUIT, DRAW, TOP, SWAP, HAND, LOOK
from game import Game

ID_K = 'id'
CONN_K = 'conn'
ADDR_K = 'addr'
NO_MSG = ''
POLL_TIME = 0.1
_NO_END_GAME = -1
GLOBAL_CHAT = ['global', 'all']

class GolfServer():
    def __init__(self, n=0):
        ''' '''
        if not (MIN_PLRS <= n <= MAX_PLRS):
            while not (MIN_PLRS <= n <= MAX_PLRS):
                n = int(raw_input('How many players: ')) 
        self.nplayers = n
        self.END_GAME = _NO_END_GAME
        self.drawn = False
        self._init_server()
        self._init_game()

        # start the player handlers
        self.tasks = []
        for c, a in self.connections:
            kwargs = {ID_K: self.connections.index((c,a)), CONN_K: c, ADDR_K: a}
            task_r = threading.Thread(target=self.recv_plr_msg, kwargs=kwargs)
            task_r.daemon = True
            self.tasks.append(task_r)
            task_p = threading.Thread(target=self.player_play, kwargs=kwargs)
            task_p.daemon = True
            self.tasks.append(task_p)

    def _init_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((HOST, PORT))
        self.connections = []
        self.r_msgs = ['' for i in range(self.nplayers)]
        while len(self.connections) < self.nplayers:
            self.s.listen(1)
            conn, addr = self.s.accept()
            if addr not in [a for c, a in self.connections]:
                self.connections.append((conn, addr))
                logging.debug('Connected by {0}'.format(addr))
            else:
                conn.sendall('Please wait for other players to connect...\n\
                             There are currently {0} players connected out of\n\
                             {1} needed.'.format(len(self.connections), self.nplayers))
        logging.debug("All players connected!")

    def _init_game(self):
        '''  '''
        game = Game(self.nplayers)
        for i in range(len(game.players)):
            name = raw_input('player {0}\'s name: '.format(i))
            game.new_player(name, i)
        game.deck.shuffle()
        game.begin()
        game.deal()
        logging.debug('%d cards in deck' % len(game.deck.cards))
        logging.debug('%d cards in discard' % len(game.deck.discards))
        self.active_card = game.deck.draw()[0]
        self.active_card.face_up()
        self.game = game

    def recv_plr_msg(self, **kwargs):
        ''' '''
        id_ = kwargs.get(ID_K)
        conn = kwargs.get(CONN_K)
        conn.sendall('Starting up player {0}!'.format(id_))
        # prompt for name
        while True:
            msg = str(conn.recv(PACKET_SIZE))
            logging.debug('received "{0}" from player {1}'.format(msg, id_))
            self.r_msgs[id_] = msg
            time.sleep(0.1)

    def player_play(self, **kwargs):
        id_ = kwargs.get(ID_K)
        conn = kwargs.get(CONN_K)
        while True:
            msg = self._get_input(id_)
            if msg in CHAT:
                self._manage_chat(id_)
            else:
                resp = NO_MSG
                if self.game.curr_plr.seat == id_:
                    resp = self._manage_active(id_, msg)
                else:
                    resp = self._manage_inactive(id_, msg)
                conn.sendall(resp)

    def _manage_chat(self, id_):
        ''' '''
        conn = self.connections[id_][0]
        conn.sendall('Who?')
        trg = self._get_input(id_)
        conn.sendall('Message: ')
        msg = self._get_input(id_)
        if trg in GLOBAL_CHAT:
            for c, a in self.connections:
                if c != conn:
                    c.sendall(msg)
        else:
            plrs = [p for p in self.game.players if p.name == trg]
            if plrs:
                for p in plrs:
                    self.connections[p.seat][0].sendall(msg)
            # silently don't send if the player doesn't exist

    def _manage_active(self, id_, msg):
        ''' '''
        def _hand(p):
            ''' '''
            resp = '{0}\'s hand:\n{1}'.format(p.name, p.hand.pretty_print())
            return resp

        def _look(players):
            ''' '''
            resp = ''
            for p in players:
                resp = resp + _hand(p)
            return resp

        def _detect_end_game(game):
            ''' Detect the end of the game by checking if all cards are flipped. '''
            if False in [c.is_face_up() for c in game.curr_plr.hand.cards]:
                return _NO_END_GAME
            else:
                return game.curr_plr.seat

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
            pos = int(self._get_input(id_))
            self.active_card = plr.hand.swap(pos, self.active_card)
            self.active_card.face_up()
            if self.END_GAME == _NO_END_GAME:
                self.END_GAME = _detect_end_game(self.game)
            self.game.next_player()
            self.drawn = False

        elif msg in HAND:
            resp = _hand(plr)

        elif msg in LOOK:
            resp = _look(self.game.players)

        elif msg in NEXT:
            self.game.next_player()
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

    def _get_input(self, id_):
        while self.r_msgs[id_] == NO_MSG:
            time.sleep(POLL_TIME)
        msg = str(self.r_msgs[id_])
        self.r_msgs[id_] = NO_MSG
        return msg


    def play(self):
        ''' '''
        for task in self.tasks:
            task.start()
        while True:
            in_ = raw_input(PROMPT)
            for c, a in ES.connections:
                c.sendall(in_)

    def score(self):
        ''' Compute and display the scores. '''
        logging.info('Game over.')
        for p in self.game.players:
            p.hand.flip_all()
            p.score = _score(p.hand)
            _hand(p)
            logging.info('{0}\'s score: {1}'.format(p.name, p.score))
        scores = [p.score for p in self.game.players]
        winner = self.game.players[scores.index(min(scores))]
        logging.info('The winner is: {0}!'.format(winner.name))

ES = GolfServer()
ES.play()
ES.score()


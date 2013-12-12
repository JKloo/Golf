#!/usr/bin/python
import os
import sys
import socket
import threading
import time
import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

from config.settings import HOST, PORT, PACKET_SIZE, PROMPT, MIN_PLRS, MAX_PLRS
from config.commands import CHAT, NEXT, QUIT, DRAW, TOP, SWAP, HAND, LOOK, HELP
from golf.golf_game import GolfGame
from comm import Server

ID_K = 'id'
CONN_K = 'conn'
ADDR_K = 'addr'

STATUS_K = 'status'
NO_CONN_S = 0
INIT_S = 1
READY_S = 2

NO_MSG = ''
POLL_TIME = 0.1


class GolfServer():
    def __init__(self, n):
        ''' '''
        self.nplayers = n
        self.end_game = False
        self.s = Server(n)
        self.player_data = self.s.search(n)
        self._init_game()

    def _init_game(self):
        '''  '''
        self.game = GolfGame(self.nplayers)
        self._init_players()
        self.game.begin(6)

    def _init_players(self):
        i = 0
        for p in self.player_data:
            self.game.players[i].name = p.NAME


    def _turn(self):
        # send the game data to each player
        self._update_players()

        # wait for input from the active player self.s.connections[self.active_player]
        m = self.s.recv(self.game.curr_player.seat)

        # handle action
        self._verify_action(m)

        # increment the active player
        self.game.next_player()

        # check for end game
        self.end_game = self._detect_end_game()

    def _update_players(self):
        """ send game information to all players. """
        self.s.send_global(self.game)

    def _verify_action(self, m):
        """ process and handle the action dict 'm'. """
        # TODO: make sure the action was allowed
        self.game = m

    def _detect_end_game(self):
        ''' Detect the end of the game by checking if all cards are flipped. '''
        return not (False in [c.is_face_up() for c in self.game.active_player.hand.cards])


    def score(self):
        ''' Compute and display the scores. '''
        logging.info('Game over.')
        logging.info('The winner is: {0}!'.format(winner.name))
        self._update_players()
        self.s.stop()


if __name__ == '__main__':
    n = int(sys.argv.get(1, 0))
    if not (MIN_PLRS <= n <= MAX_PLRS):
            while not (MIN_PLRS <= n <= MAX_PLRS):
                n = int(raw_input('How many players: '))
    ES = GolfServer(n)
    ES.play()
    ES.score()
    for t in ES.tasks:
        logging.debug(t.name)
        logging.debug(t.is_alive())

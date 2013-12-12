#!/usr/bin/python

from copy import deepcopy

from cardgame.game import Game
from golf_player import GolfPlayer, NO_PLAYER
from golf_deck import GolfDeck


class GolfGame(Game):
    def __init__(self, nplayers, ndecks=1):
        ''' '''
        self.nplayers = nplayers
        self.deck = GolfDeck()
        self.players = [deepcopy(NO_PLAYER) for i in range(nplayers)]
        self.active_player = self.players[0]
        self.active_card = None

    def new_player(self, name, seat):
        ''' '''
        if NO_PLAYER in self.players:
            if (seat >= len(self.players)) or not (self.players[seat] == NO_PLAYER):
                # if the seat preference is taken, seat in the minimum available seat
                seat = min([x for x in range(len(self.players)) if self.players[x] == NO_PLAYER])
            self.players[seat] = GolfPlayer(name, seat)

    def next_card(self):
        if self.active_card:
            self.deck.

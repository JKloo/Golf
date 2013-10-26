#!/usr/bin/env python

from player import Player, NO_PLAYER
from deck import Deck

class Game:
    ''' '''
    def __init__(self, nplayers, ndecks=1):
        ''' '''
        self.deck = Deck()
        self.players = [NO_PLAYER for i in range(nplayers)]
        self.curr_plr = self.players[0]

    def deal(self):
        ''' '''
        for p in self.players:
            p.hand.cards = self.deck.draw(6)

    def new_player(self, name, seat):
        ''' '''
        if NO_PLAYER in self.players:
            if (seat >= len(self.players)) or not (self.players[seat] == NO_PLAYER):
                # if the seat preference is taken, seat in the minimum available seat
                seat = min([x for x in range(len(self.players)) if self.players[x] == NO_PLAYER])
            self.players[seat] = Player(name, seat)

    def _next_player(self):
        ''' '''
        id_ = self.players.index(self.curr_plr)
        if id_ == len(self.players):
            id_ = 0
        else:
            id_ += 1
        self.curr_plr = self.players[id_]

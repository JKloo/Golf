#!/usr/bin/env python
from copy import deepcopy
from player import Player, NO_PLAYER
from deck import Deck

class Game:
    ''' '''
    def __init__(self, nplayers, ndecks=1):
        ''' '''
        self.deck = Deck()
        self.players = [deepcopy(NO_PLAYER) for i in range(nplayers)]
        self.curr_plr = self.players[0]

    def begin(self, ncards):
        ''' '''
        self.curr_plr = self.players[0]
        self.deck.shuffle()
        self.deal(ncards)

    def deal(self, n):
        ''' '''
        for p in self.players:
            p.hand.cards = self.deck.draw(n)

    def new_player(self, name, seat):
        ''' '''
        if NO_PLAYER in self.players:
            if (seat >= len(self.players)) or not (self.players[seat] == NO_PLAYER):
                # if the seat preference is taken, seat in the minimum available seat
                seat = min([x for x in range(len(self.players)) if self.players[x] == NO_PLAYER])
            self.players[seat] = Player(name, seat)

    def next_player(self):
        ''' '''
        id_ = self.players.index(self.curr_plr)
        id_ += 1
        if id_ >= len(self.players):
            id_ = 0      
        self.curr_plr = self.players[id_]

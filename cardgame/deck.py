#!/usr/bin/python

import random
import copy
from card import Card, JOKER_CARD


class Deck:
    ''' '''
    SUITS = 'HDSC'
    NS = '123456789TJQK'

    def __init__(self, ns=NS, suits=SUITS, njokers=0):
        self.cards = []
        self.discards = self.create(ns, suits, njokers)

    def create(self, ns, suits, njokers):
        ''' '''
        _cards = [Card(n, s) for n in ns for s in suits]
        _cards.extend([copy.deepcopy(JOKER_CARD) for i in range(njokers)])
        return _cards

    def shuffle(self):
        ''' '''
        # shuffle between 4 and 10 times
        for i in range(random.randrange(4, 10)):
            random.shuffle(self.discards)
        self.cards.extend(self.discards)
        self.discards = []
        for c in self.cards:
            c.face_down()

    def draw(self, n=1):
        ''' '''
        if self.cards:
            return [self.cards.pop(0) for x in range(n)]
        elif self.discards:
            print 'shuffling'
            self.shuffle()
            self.draw(n)
        else:
            raise ValueError('empty stack!')

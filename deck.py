#!/usr/bin/env python

import random
from card import Card

class Deck:
    ''' '''
    SUITS = 'HDSC'
    NS = '123456789TJQKW'
    def __init__(self):
        self.cards = []
        self.discards = self.create(self.NS, self.SUITS)
        
    def create(self, ns, suits):
        ''' '''
        return [Card(n,s) for n in ns for s in suits]

    def shuffle(self):
        ''' '''
        # shuffle between 4 and 10 times
        for i in range(random.randrange(4,10)):
            random.shuffle(self.discards)
        self.cards.extend(self.discards)
        self.discards = []

    def draw(self, n=1):
        ''' '''
        if self.cards:
            return [self.cards.pop(0) for x in range(n)]
        else:
            raise ValueError('empty stack!')

#!/usr/bin/env python

import random
import copy
import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

class Card:
'''
'''
    def __init__(self, n, suit):
        self.n = n
        self.suit = suit

class Deck:
'''
'''
    def __init__(self):
        SUITS = 'HDSC'
        NS = '123456789TJQKW'
        self.cards = create_deck(NS, SUITS)
        self.discards = []
        
    def create_deck(ns, suits):
        '''
        '''
        return [Card(n,s) for n in ns for s in suits]

    def shuffle_deck(self):
        '''
        '''
        # shuffle between 4 and 10 times
        for i in range(random.randrange(4,10)):
            random.suffle(self.discard)
        self.cards.extend(self.discard)
        self.discard = []

    def draw_card(self):
        '''
        '''
        if cards:
            cards.pop(0)
        else:
            raise ValueError('empty stack!')

class Board:
    '''
    '''
    def __init__(self, cards=list()):
        '''
        '''
        self.cards = cards
        self.pairs = [(0, 3), (1, 4), (2, 5)]


    def swap(self, pos, card):
        '''
        '''
        card_ = self.cards.pop(pos)
        self.cards.insert(pos, card)
        return card_

class Player:
    '''
    '''
    def __init__(self, name, seat):
        '''
        '''
        self.name = name
        self.seat = seat
        self.board = None


class Game:
    '''
    '''
    def __init__(self, nplayers, ndecks=1):
        '''
        '''
        self.nseats = nplayers
        self.empty_seats = range(nplayers)
        self.deck = Deck()
        self.players = [None for i in nplayers]

    def new_player(self, name, seat):
        if self.empty_seats:
            

    def _next_player(self)




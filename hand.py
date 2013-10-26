#!/usr/bin/env python
from card import JOKER_CARD as JC

class Hand:
    ''' '''
    def __init__(self, cards=list()):
        ''' '''
        self.cards = cards
        self.pairs = [(0, 3), (1, 4), (2, 5)]
        # self.revealed = [False for i in range(len(cards))]

    def __str__(self):
        ''' '''
        return '{0}, {1}, {2} \n{3}, {4}, {5}'.format(*[str(x) for x in self.cards])

    def swap(self, pos, card):
        ''' '''
        card_ = self.cards.pop(pos)
        self.cards.insert(pos, card)
        return card_

    def flip_all(self):
        ''' '''
        for c in self.cards:
            c.face_up()

    def match(self, x, y):
        ''' '''
        x_c = self.cards[x]
        y_c = self.cards[y]
        # Two Jokers should not match, compare by name
        return (x_c.get_name() == y_c.get_name()) and not (x_c.get_name() == JC.get_name())
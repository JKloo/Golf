#!/usr/bin/env python

class Hand:
    ''' '''
    def __init__(self, cards=list()):
        ''' '''
        self.cards = cards
        self.pairs = [(0, 3), (1, 4), (2, 5)]
        self.revealed = [False for i in range(len(cards))]

    def __str__(self):
        ''' '''
        return '{0}, {1}, {2} \n{3}, {4}, {5}'.format(*[str(x) for x in self.cards])

    def swap(self, pos, card):
        ''' '''
        card_ = self.cards.pop(pos)
        self.cards.insert(pos, card)
        return card_
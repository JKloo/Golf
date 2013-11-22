#!/usr/bin/python
from card import JOKER_CARD as JC


class Hand:
    ''' '''
    def __init__(self, cards=list()):
        ''' '''
        self.cards = cards

    def __str__(self):
        ''' '''
        return ', '.join([str(x) for x in self.cards])

    def swap(self, pos, card):
        ''' '''
        card_ = self.cards.pop(pos)
        self.cards.insert(pos, card)
        return card_

    def flip_all(self):
        ''' '''
        for c in self.cards:
            c.face_up()

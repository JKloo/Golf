#!/usr/bin/python

import sys

from cardgame.deck import Deck


class GolfDeck(Deck):
    def __init__(self):
        Deck.__init__(self, njokers=2)

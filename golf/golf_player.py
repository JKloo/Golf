#!/usr/bin/python

import sys

from cardgame.player import Player
from golf_hand import GolfHand


class GolfPlayer(Player):
    def __init__(self, name, seat):
        self.name = name
        self.seat = seat
        self.hand = GolfHand()
        self.score = 0
        self.other = {'drawn': False}

    def score(self, flipall=False):
        if flipall:
            self.hand.flip_all()
        

NO_PLAYER = GolfPlayer('', -1)

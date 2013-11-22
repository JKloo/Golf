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
        self.other = {}

NO_PLAYER = GolfPlayer('', -1)

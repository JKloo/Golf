import sys

from cardgame.hand import Hand

class GolfHand(Hand):
    PAIRS = [(0, 3), (1, 4), (2, 5)]
    BLOCKS = [(0, 1, 3, 4), (1, 2, 4, 5)]

    def __init__(self, cards=list()):
        Hand.__init__(self, cards)

    def __str__(self):
        ''' '''
        return '{0}, {1}, {2} \n{3}, {4}, {5}'.format(*[str(x) for x in self.cards])

    def pretty_print(self):
        _cards = [c.pretty_print().split('\n') for c in self.cards]
        _top = ['{0} {1} {2}'.format(_cards[0][x], _cards[1][x], _cards[2][x]) for x in range(len(_cards[0]))]
        _bot = ['{0} {1} {2}'.format(_cards[3][x], _cards[4][x], _cards[5][x]) for x in range(len(_cards[3]))]
        return '\n'.join(['\n'.join(_top), '\n'.join(_bot)])

    def match(self, *args):
        ''' '''
        _cs = [self.cards[x] for x in args]
        _m = [x == y for x in _cs for y in _cs]
        return not False in _m

    def score(self):
        ''' Compute a player's score. '''
        _s = 0
        for cs in self.BLOCKS:
            if self.match(*cs):
                _s -= 20
        for cs in self.PAIRS:
            if not self.match(*cs):
                _s += sum([int(self.cards[x]) for x in cs])
        return _s

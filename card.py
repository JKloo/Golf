_JOKER = 'W'
_WIDTH = 8
_SPACE = ''.join([' ' for i in range(_WIDTH)])
_PRETTY = '\
+--------+\n\
|        |\n\
|{0}|\n\
|   of   |\n\
|{1}|\n\
|        |\n\
+--------+'

_BLANK = '\
+--------+\n\
|XXXXXXXX|\n\
|XXXXXXXX|\n\
|XXXXXXXX|\n\
|XXXXXXXX|\n\
|XXXXXXXX|\n\
+--------+'

SPADE = u'\u2660'
HEART = u'\u2661'
DIAMOND = u'\u2662'
CLUB = u'\u2663'

def _pad(s, l):
    if len(s) < l:
        s = ' ' + s + ' '
        return _pad(s, l) 
    else:
        return s[:8]

class Card:
    ''' '''
    SUITS = {'H': 'Hearts', 'D': 'Diamonds', 'C': 'Clubs', 'S': 'Spades', _JOKER: 'Wild'}
    CARD_NAMES = {'1': 'Ace', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7',
                  '8': '8', '9': '9', 'T': '10', 'J': 'Jack', 'Q': 'Queen', 'K': 'King', _JOKER: 'Joker'}
    CARD_POINTS = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                   '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 0, _JOKER: -2}
    def __init__(self, n, s):
        self._n = n
        self.n = self.CARD_NAMES[n]
        self._s = s
        self.suit = self.SUITS[s]
        self._up = False

    def __str__(self):
        HIDDEN = '-----------' 
        return '{0} of {1}'.format(self.get_name(), self.get_suit()) if self._up else HIDDEN

    def __int__(self):
        return self.get_points()

    def __eq__(self, other):
        ''' '''
        if isinstance(other, Card):
            return self.get_name() == other.get_name()
        return NotImplemented

    def __ne__(self, other):
        ''' '''
        r = self.__eq__(other)
        if r is NotImplemented:
            return r
        return not r

    def pretty_print(self):
        ''' '''
        if self._up:
            return _PRETTY.format(_pad(self.n, _WIDTH), _pad(self.suit, _WIDTH))
        else:
            return _BLANK

    def face_up(self):
        self._up = True

    def face_down(self):
        self._up = False

    def is_face_up(self):
        return self._up

    def is_face_down(self):
        return not self.is_face_up()

    def get_suit(self):
        return self.SUITS[self._s]

    def get_name(self):
        return self.CARD_NAMES[self._n]

    def get_points(self):
        return self.CARD_POINTS[self._n]

JOKER_CARD = Card(_JOKER, _JOKER)

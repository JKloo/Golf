import defaults.def_card as defc
import ui.ui_card as uic


class Card:
    ''' '''
    def __init__(self, n, s):
        self._n = n
        self.n = defc.CARD_NAMES[n]
        self._s = s
        self.suit = defc.SUITS[s]
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
        return uic.pretty_print(self._up, self.get_name(), self.get_suit())


    def face_up(self):
        self._up = True


    def face_down(self):
        self._up = False


    def is_face_up(self):
        return self._up


    def is_face_down(self):
        return not self.is_face_up()


    def get_suit(self):
        return defc.SUITS[self._s]


    def get_name(self):
        return defc.CARD_NAMES[self._n]


    def get_points(self):
        return defc.CARD_POINTS[self._n]


JOKER_CARD = Card(defc._JOKER, defc._JOKER)

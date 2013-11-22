from hand import Hand


class Player:
    ''' '''
    def __init__(self, name, seat):
        ''' '''
        self.name = name
        self.seat = seat
        self.hand = Hand()
        self.score = 0
        self.other = {}

NO_PLAYER = Player('', -1)

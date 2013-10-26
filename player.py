from hand import Hand

NO_PLAYER = -1

class Player:
    ''' '''
    def __init__(self, name, seat):
        ''' '''
        self.name = name
        self.seat = seat
        self.hand = Hand()
        self.score = 0

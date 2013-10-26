#!/usr/bin/env python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

from game import Game

def setup():
    ''' '''
    MIN_PLRS = 1
    MAX_PLRS = 4
    n = MIN_PLRS - 1
    while not (MIN_PLRS <= n <= MAX_PLRS):
        n = int(raw_input('How many players: '))
    game = Game(n)
    for i in range(len(game.players)):
        name = raw_input('player %d\'s name: ' % i)
        seat = int(raw_input('player %d\'s seat: ' % i))
        game.new_player(name, seat)
    game.deck.shuffle()
    game.deal()
    logging.info('%d cards in deck' % len(game.deck.cards))
    logging.info('%d cards in discard' % len(game.deck.discards))
    for p in game.players:
        logging.info('%s\'s hand:' % p.name)
        logging.info(str(p.hand))

def play():
    ''' '''
    pass

if __name__ == '__main__':
    setup()


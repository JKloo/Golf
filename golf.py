#!/usr/bin/env python

import sys
import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

from game import Game

NEXT = ['n', 'next']
QUIT = ['q', 'quit']
DRAW = ['d', 'done']
TOP = ['t', 'top']
SWAP = ['s', 'swap']
HAND = ['h', 'hand']
LOOK = ['l', 'look']
SEP = '============================='
_NO_END_GAME = -1


def setup():
    ''' '''
    MIN_PLRS = 1
    MAX_PLRS = 4
    n = MIN_PLRS - 1
    while not (MIN_PLRS <= n <= MAX_PLRS):
        n = int(raw_input('How many players: '))
    game = Game(n)
    for i in range(len(game.players)):
        name = raw_input('player {0}\'s name: '.format(i))
        seat = int(raw_input('player {0}\'s seat: '.format(i)))
        game.new_player(name, seat)
    game.deck.shuffle()
    game.begin()
    game.deal()
    logging.info('%d cards in deck' % len(game.deck.cards))
    logging.info('%d cards in discard' % len(game.deck.discards))
    _look(game.players)
    return game

def play(game):
    ''' '''
    END_GAME = _NO_END_GAME

    for p in game.players:
        logging.info('{0}, choose two cards to flip:'.format(p.name))
        a = int(raw_input('>> card 1: '))
        b = int(raw_input('>> card 2: '))
        p.hand.cards[a].face_up()
        p.hand.cards[b].face_up()

    active_card = game.deck.draw()[0]
    active_card.face_up()
    while game.curr_plr.seat != END_GAME:
        # Alert current player
        logging.info(SEP)
        logging.info('{0}\'s turn.'.format(game.curr_plr.name))
        drawn = False
        in_ = ''
        # Wait for player input
        while in_ not in NEXT:
            in_ = _player_input()
            # Handle player input
            if in_ in QUIT:
                _quit()
            elif in_ in DRAW and not drawn:
                drawn = True
                game.deck.discards.append(active_card)
                active_card = game.deck.draw()[0]
                active_card.face_up()
                logging.info(str(active_card))
            elif in_ in TOP:
                logging.info(str(active_card))
            elif in_ in SWAP:
                pos = int(raw_input('>> pos: '))
                active_card = game.curr_plr.hand.swap(pos, active_card)
                active_card.face_up()
                if END_GAME == _NO_END_GAME:
                    END_GAME = _detect_end_game(game)
                in_ = NEXT[0]
            elif in_ in HAND:
                _hand(game.curr_plr)
            elif in_ in LOOK:
                _look(game.players)
        # Select next player
        game.next_player()
    return game

def score(game):
    ''' Compute and display the scores. '''
    logging.info('Game over.')
    for p in game.players:
        p.hand.flip_all()
        p.score = _score(p.hand)
        _hand(p)
        logging.info('{0}\'s score: {1}'.format(p.name, p.score))
    scores = [p.score for p in game.players]
    winner = game.players[scores.index(min(scores))]
    logging.info('The winner is: {0}!'.format(winner.name))

def _player_input():
    return raw_input('>> ')

def _quit():
    ''' '''
    logging.info('Quitting Game...')
    sys.exit(0)

def _detect_end_game(game):
    ''' Detect the end of the game by checking if all cards are flipped. '''
    if False in [c.is_face_up() for c in game.curr_plr.hand.cards]:
        return _NO_END_GAME
    else:
        return game.curr_plr.seat

def _hand(p):
    ''' '''
    logging.info('{0}\'s hand:'.format(p.name))
    logging.info(str(p.hand))

def _look(players):
    ''' '''
    for p in players:
        _hand(p)

def _score(hand):
    ''' Compute a player's score. '''
    _s = 0
    for x, y in hand.pairs:
        if not hand.match(x, y):
            _s += int(hand.cards[x]) + int(hand.cards[y])
    return _s

if __name__ == '__main__':
    game = setup()
    play(game)
    score(game)

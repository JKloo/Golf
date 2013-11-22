#!/usr/bin/python


class _Command:
    def __init__(self, cmds, help):
        self.cmds = cmds
        self.help = help

    def __str__(self):
        return 'Enter {0} to {1}\n'.format(' or '.join(['\"{0}\"'.format(c) for c in self.cmds]), self.help)

    def __contains__(self, c):
        return c in self.cmds

CHAT = _Command(['c', 'chat'], 'chat a message to a player or to everyone. Prompts for user to message, then for message.')
NEXT = _Command(['p', 'pass'], 'end your turn without swapping the top card.')
QUIT = _Command(['q', 'quit'], 'quit the game.')
DRAW = _Command(['d', 'draw'], 'draw the top card off the deck.')
TOP  = _Command(['t', 'top'],  'look at the card face up.')
SWAP = _Command(['s', 'swap'], 'swap the face up card with one in your hand. Prompts for the position of the card to swap (0-indexed)')
HAND = _Command(['h', 'hand'], 'look at your hand.')
LOOK = _Command(['l', 'look'], 'look at everone\'s hands')
HELP = _Command(['help'], 'show this help message')

CHAT_P = r'@([\w]+): (.+)'
SWAP_P = r's|(?:swap) (\d)'

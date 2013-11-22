
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

_SPADE = u'\u2660'
_HEART = u'\u2661'
_DIAMOND = u'\u2662'
_CLUB = u'\u2663'


def _pad(s, l):
    if len(s) < l:
        s = ' ' + s + ' '
        return _pad(s, l)
    else:
        return s[:8]


def pretty_print(up, n, s):
    ''' '''
    if up:
        return _PRETTY.format(_pad(n, _WIDTH),
                              _pad(s, _WIDTH))
    else:
        return _BLANK

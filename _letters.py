"""Copyright Michael A. Ciociola
GPLv3
"""

from dragonfly import (
    MappingRule,
    AppContext,
    IntegerRef,
    Grammar,
    Key,
)

letterMap = {
    "(A|alpha)": "a",
    "(B|bravo) ": "b",
    "(C|charlie) ": "c",
    "(D|delta) ": "d",
    "(E|echo) ": "e",
    "(F|foxtrot) ": "f",
    "(G|golf) ": "g",
    "(H|hotel) ": "h",
    "(I|india|indigo) ": "i",
    "(J|juliet) ": "j",
    "(K|kilo) ": "k",
    "(L|lima) ": "l",
    "(M|mike) ": "m",
    "(N|november) ": "n",
    "(O|oscar) ": "o",
    "(P|papa|poppa) ": "p",
    "(Q|quebec|quiche) ": "q",
    "(R|romeo) ": "r",
    "(S|sierra) ": "s",
    "(T|tango) ": "t",
    "(U|uniform) ": "u",
    "(V|victor) ": "v",
    "(W|whiskey) ": "w",
    "(X|x-ray) ": "x",
    "(Y|yankee) ": "y",
    "(Z|zulu) ": "z",
}

rules = MappingRule (
    mapping = letterMap
)

grammar = Grammar("letters")
grammar.add_rule(rules)
grammar.load()


def unload():
    """Unload function which will be called at unload time."""
    global grammar
    if grammar:
        grammar.unload()
    grammar = None

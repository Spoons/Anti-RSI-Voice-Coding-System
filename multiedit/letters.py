"""Copyright Michael A. Ciociola
GPLv3
"""

from dragonfly import (
    MappingRule,
    AppContext,
    IntegerRef,
    RuleRef,
    Alternative,
    Grammar,
    Repetition,
    CompoundRule,
    Rule,
    Key,
)

letterMap = {
    "(alpha)": Key("a"),
    "(bravo) ": Key("b"),
    "(charlie) ": Key("c"),
    "(delta) ": Key("d"),
    "(echo) ": Key("e"),
    "(foxtrot) ": Key("f"),
    "(golf) ": Key("g"),
    "(hotel) ": Key("h"),
    "(india|indigo) ": Key("i"),
    "(juliet) ": Key("j"),
    "(kilo) ": Key("k"),
    "(lima) ": Key("l"),
    "(mike) ": Key("m"),
    "(november) ": Key("n"),
    "(oscar) ": Key("o"),
    "(papa|poppa) ": Key("p"),
    "(quebec|quiche) ": Key("q"),
    "(romeo) ": Key("r"),
    "(sierra) ": Key("s"),
    "(tango) ": Key("t"),
    "(uniform) ": Key("u"),
    "(victor) ": Key("v"),
    "(whiskey) ": Key("w"),
    "(x-ray) ": Key("x"),
    "(yankee) ": Key("y"),
    "(zulu) ": Key("z"),
}
class LettersRule(MappingRule):
    mapping = letterMap




alternatives = []
alternatives.append(RuleRef(rule=LettersRule()))

single_action = Alternative(alternatives)

new_sequence = Repetition(single_action, min=1, max=16, name="new_sequence")

class LetterRepeter(CompoundRule):
    spec = "spell <new_sequence>"
    extras = [
        new_sequence
    ]

    def _process_recognition(self, node, extras):
        new_sequence = extras["new_sequence"]
        for action in new_sequence:
            action.execute()


grammar = Grammar("letters")
grammar.add_rule(LetterRepeter())
grammar.load()


def unload():
    """Unload function which will be called at unload time."""
    global grammar
    if grammar:
        grammar.unload()
    grammar = None

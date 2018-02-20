from dragonfly import (
    CompoundRule,
    MappingRule,
    RuleRef,
    Repetition,
    Dictation,
    IntegerRef,
    Grammar
)

from lib.dynamic_aenea import (
    GlobalDynamicContext,
    Key,
    Text,
)

class SeriesMappingRule(CompoundRule):

    def __init__(self, mapping, extras=None, defaults=None):
        mapping_rule = MappingRule(mapping=mapping, extras=extras,
                                   defaults=defaults, exported=False)
        single = RuleRef(rule=mapping_rule)
        series = Repetition(single, min=1, max=16, name="series")

        compound_spec = "<series>"
        compound_extras = [series]
        CompoundRule.__init__(self, spec=compound_spec,
                              extras=compound_extras, exported=True)

    def _process_recognition(self, node, extras):  # @UnusedVariable
        series = extras["series"]
        for action in series:
            action.execute()

series_rule = SeriesMappingRule(
    mapping={
        # Filler words.
        "foobar": Text("foobar"),
        "foo": Text("foo"),
        "bar": Text("bar"),
        # File extensions.
        "dot C S": Text(".cs"),
        "dot css": Text(".css"),
        "dot J S": Text(".js"),
        "dot jar": Text(".jar"),
        "dot (py|pie|P Y)": Text(".py"),
        "dot (ruby|R B)": Text(".rb"),
        "dot (rar|R A R)": Text(".rar"),
        "dot S H": Text(".sh"),
        "dot T X T": Text(".txt"),
        # Non mainstream web url extensions.
        "dot (O R G|org)": Text(".org"),
        # Protocols.
        "protocol H T T P": Text("http://"),
        "protocol H T T P S": Text("https://"),
        "protocol (git|G I T)": Text("git://"),
        "protocol F T P": Text("ftp://"),
        "protocol S S H": Text("ssh://"),
        },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
        ],
    defaults={
        "n": 1
    }
)

grammar = Grammar("Programming help", context=GlobalDynamicContext())
grammar.add_rule(series_rule)
grammar.load()


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None

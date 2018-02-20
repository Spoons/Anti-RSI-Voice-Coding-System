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

from rules.series_mapping import SeriesMappingRule

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

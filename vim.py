from dragonfly import (
    Grammar, 
    IntegerRef, 
    Choice, 
    AppContext, 
    MappingRule, 
    Dictation, 
    Key, 
    Text, 
    Function
)

import lib.format


vim_context = AppContext(executable="mintty.exe")
grammar = Grammar("vim", context=vim_context)

#from _generic_edit import pressKeyMap

pressKeyMap = {}


surroundCharsMap = {
    'quotes': '"',
    'parens': "(",
    'brackets': "[",
    'braces': "{",
}


def goto_line(n):
    for c in str(n):
        Key(c).execute()
    Key("G").execute()


def yank_lines(n, n2):
    goto_line(n)
    Key("V").execute()
    goto_line(n2)
    Key("y").execute()

def delete_lines(n, n2):
    goto_line(n)
    Key("V").execute()
    goto_line(n2)
    Key("d").execute()


basics_mapping = {
    'mup <n> [le|lines|line]': Key("escape, up:%(n)d"),
    'dom <n> [le|lines|line]': Key("escape, down:%(n)d"),
    'lem <n> [line]': Key("escape, left:%(n)d"),
    'rem <n> [line]': Key("escape, right:%(n)d"),
    'go <n> [line]': Key("escape") + Function(goto_line),
    'glue': Key("escape") + Key("p"),
    'glue be': Key("escape, P"),
    'escape': Key("escape"),
    'insert': Key("i"),
    'insert before': Key("I"),
    'insert below': Key("o"),
    'insert above': Key("O"),
    'append': Key("A"),
    'undo' : Key("escape, u"),
    'redo' : Key("escape, c-r"),
    'slap' : Key("enter")
}

def define_function(text):
    Text("def ").execute()
    lib.format.snake_case_text(text)
    Text("():").execute()
    Key("left:2").execute()


def define_method(text):
    Text("def ").execute()
    lib.format.snake_case_text(text)
    Text("(self, ):").execute()
    Key("left:2").execute()


def define_class(text):
    Text("class ").execute()
    lib.format.pascal_case_text(text)
    Text("():").execute()
    Key("left:2").execute()


class PythonGrammar(MappingRule):
    mapping = {
        "def <text>": Function(define_function),
        'print' : Text("print()") + Key("left")
    }
    extras = [
        Dictation("text")
    ]

class VimSymbols(MappingRule):
    mapping = {
        'at': Key('at'),
        'close arc': Key('rparen'),
        'close curly': Key('rbrace'),
        'close square': Key('rbracket'),
        'colon': Key('colon'),
        'comma': Key('comma'),
        'dot': Key('dot'),
        'hash': Key('hash'),
        'open arc': Key('lparen'),
        'open curly': Key('lbrace'),
        'open square': Key('lbracket'),
        'percent': Key('percent'),
        'plus': Key('plus'),
        'slash': Key('slash'),
    }

class VimGroupingSymbols(MappingRule):
    mapping = {
        'angle': Key('langle, rangle, left'),
        'arc': Key('lparen, rparen, left'),
        'curly': Key('lbrace, rbrace, left'),
        'double': Key('dquote, dquote, left'),
        'single': Key('squote, squote, left'),
        'square': Key('lbracket, rbracket, left'),
    }

basics_rule = MappingRule(
    mapping = basics_mapping,
    extras = [
        Dictation('text'),
        IntegerRef('n', 1, 999),
        IntegerRef('n2', 1, 999),
        Choice("pressKey", pressKeyMap),
        Choice("surroundChar", surroundCharsMap),
            ],
        )


grammar.add_rule(basics_rule)
grammar.add_rule(VimSymbols())
grammar.add_rule(VimGroupingSymbols())
grammar.add_rule(PythonGrammar())
grammar.load()



def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None



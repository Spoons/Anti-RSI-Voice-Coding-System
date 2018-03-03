# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

try:
    import pkg_resources
    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

from dragonfly import *
from maps import maps


config = Config("multi edit")
config.cmd = Section("Language section")
namespace = config.load()


#---------------------------------------------------------------------------
# Here we prepare the list of formatting functions from the config file.

# Retrieve text-formatting functions from this module's config file.
#  Each of these functions must have a name that starts with "format_".
format_functions = {}
if namespace:
    for name, function in namespace.items():
        if name.startswith("format_") and callable(function):
            spoken_form = function.__doc__.strip()

        # We wrap generation of the Function action in a function so
        #  that its *function* variable will be local.  Otherwise it
        #  would change during the next iteration of the namespace loop.
        def wrap_function(function):
            def _function(dictation):
                formatted_text = function(dictation)
                Text(formatted_text).execute()
            return Function(_function)

        action = wrap_function(function)
        format_functions[spoken_form] = action


# Here we define the text formatting rule.
# The contents of this rule were built up from the "format_*"
#  functions in this module's config file.
if format_functions:
    class FormatRule(MappingRule):

        mapping  = format_functions
        extras   = [Dictation("dictation")]

else:
    FormatRule = None


class KeystrokeRule(MappingRule):

    exported = False

    mapping  = maps.key_action_map
    extras   = [
            IntegerRef("n", 1, 100),
            Dictation("text"),
            Dictation("text2"),
            ]
    defaults = {
            "n": 1,
            }



alternatives = []
alternatives.append(RuleRef(rule=KeystrokeRule()))
if FormatRule:
    alternatives.append(RuleRef(rule=FormatRule()))
ksr = Alternative(alternatives)


#class CharacterRule(MappingRule):
#    name = "CharacterRule"
#    mapping = {
#            "plain <chars>": Text("%(chars)s"),
#            "numbers <numerals>": Text("%(numerals)s"),
#            "print <letters>": Text("%(letters)s"),
#            "shout <letters>": Function(lambda letters: Text(letters.upper()).execute()),
#            }
#    extras = [
#            "numerals": numbers_element,
#            "letters": letters_element,
#            "chars": chars_element
#            ]

class RepeatRule(CompoundRule):

        # Here we define this rule's spoken-form and special elements.
    spec     = "<sequence> [[[and] repeat [that]] <n> times]"
    extras   = [
            Repetition(ksr, min=1, max=5, name="sequence"),
            IntegerRef("n", 1, 100),  # Times to repeat the sequence.
            ]
    defaults = {
            "n": 1,                   # Default repeat count.
            }

    def _process_recognition(self, node, extras):
        sequence = extras["sequence"]   # A sequence of actions.
        count = extras["n"]             # An integer repeat count.
        for i in range(count):
            for action in sequence:
                action.execute()
        maps.release.execute()


#---------------------------------------------------------------------------
# Create and load this module's grammar.

grammar = Grammar("multi edit")   # Create this module's grammar.
grammar.add_rule(RepeatRule())    # Add the top-level rule.
grammar.load()                    # Load the grammar.

# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None

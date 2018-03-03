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
import character_maps
from action_maps import key_action_maps
import lib.dragonfly_libs


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


# Rule for spelling a word letter by letter and formatting it.
spell_format_rule = utils.create_rule(
        "SpellFormatRule",
        dict([("spell " + k, v)
            for (k, v) in format_functions.items()]),
        {"dictation": letters_element}
        )

# Rule for printing a sequence of characters.
character_rule = utils.create_rule(
        "CharacterRule",
        character_action_map,
        {
            "numerals": numbers_element,
            "letters": letters_element,
            "chars": chars_element,
            }
        )

#single_action = RuleRef(rule=utils.create_rule("CommandKeystrokeRule",
#    key_action_map.command_action_map, key_action_map.keystroke_element_map))



#---------------------------------------------------------------------------
# Here we define the top-level rule which the user can say.

# This is the rule that actually handles recognitions. 
#  When a recognition occurs, it's _process_recognition() 
#  method will be called.  It receives information about the 
#  recognition in the "extras" argument: the sequence of 
#  actions and the number of times to repeat them.
class RepeatRule(CompoundRule):

    # Here we define this rule's spoken-form and special elements.
    spec     = "<sequence> [[[and] repeat [that]] <n> times]"
    extras   = [
            sequence,                 # Sequence of actions defined above.
            IntegerRef("n", 1, 100),  # Times to repeat the sequence.
            ]
    defaults = {
            "n": 1,                   # Default repeat count.
            }

    # This method gets called when this rule is recognized.
    # Arguments:
    #  - node -- root node of the recognition parse tree.
    #  - extras -- dict of the "extras" special elements:
    #     . extras["sequence"] gives the sequence of actions.
    #     . extras["n"] gives the repeat count.
    def _process_recognition(self, node, extras):
        sequence = extras["sequence"]   # A sequence of actions.
        count = extras["n"]             # An integer repeat count.
        for i in range(count):
            for action in sequence:
                action.execute()
        action_maps.release.execute()


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

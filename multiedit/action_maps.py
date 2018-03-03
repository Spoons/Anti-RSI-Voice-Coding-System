from dragonfly import *
import lib.dragonfly_libs as utils

class key_action_maps:
    release = Key("shift:up, ctrl:up")
    key_action_map = {
            # Spoken-form    ->    ->    ->     Action object
            "up [<n>]":                         Key("up/5:%(n)d"),
            "down [<n>]":                       Key("down/5:%(n)d"),
            "left [<n>]":                       Key("left/5:%(n)d"),
            "right [<n>]":                      Key("right/5:%(n)d"),
            "page up [<n>]":                    Key("pgup/5:%(n)d"),
            "page down [<n>]":                  Key("pgdown/5:%(n)d"),
            "up <n> (page | pages)":            Key("pgup/5:%(n)d"),
            "down <n> (page | pages)":          Key("pgdown/5:%(n)d"),
            "left <n> (word | words)":          Key("c-left/5:%(n)d"),
            "right <n> (word | words)":         Key("c-right/5:%(n)d"),
            "left word":                        Key("c-left/5"),
            "right word":                       Key("c-right/5"),
            "top":                              Key("home"),
            "pown":                             Key("end"),
            "doc home":                         Key("c-home"),
            "doc end":                          Key("c-end"),

            "space [<n>]":                      release + Key("space:%(n)d"),
            "enter [<n>]":                      release + Key("enter:%(n)d"),
            "cancel|escape":                    release + Key("escape"),
            #"edit text": utils.RunApp("notepad"),

            "crack [<n>]":                      release + Key("del:%(n)d"),
            "delete [<n> | this] (line|lines)": release + Key("home, s-down/5:%(n)d, del"),
            "snap [<n>]":                       release + Key("backspace/5:%(n)d"),
            "pop up":                           release + Key("apps"),

            "paste":                            release + Key("c-v"),
            "duplicate <n>":                    release + Key("c-c, c-v:%(n)d"),
            "copy":                             release + Key("c-c"),
            "cut":                              release + Key("c-x"),
            "select all":                       release + Key("c-a"),

            "[hold] shift":                     Key("shift:down"),
            "release shift":                    Key("shift:up"),
            "[hold] control":                   Key("ctrl:down"),
            "release control":                  Key("ctrl:up"),
            "release [all]":                    release,

            "say <text>":                       release + Text("%(text)s"),
            "mimic <text>":                     release + Mimic(extra="text"),
            }

    character_action_map = {
            "plain <chars>": Text("%(chars)s"),
            "numbers <numerals>": Text("%(numerals)s"),
            "print <letters>": Text("%(letters)s"),
            "shout <letters>": Function(lambda letters: Text(letters.upper()).execute()),
            }

    global_key_action_map = {
        "slap [<n>]": Key("enter/5:%(n)d"),
        "spooce [<n>]": Key("space/5:%(n)d"),
        "tab [<n>]": Key("tab/5:%(n)d"),
    }

    global_action_map = utils.combine_maps(global_key_action_map,
            utils.text_map_to_action_map(symbol_map))

    command_action_map = utils.combine_maps(global_action_map, key_action_map)

    keystroke_element_map = {
            "n": (IntegerRef(None, 1, 21), 1),
            "text": Dictation(),
            "char": DictListRef(None, char_dict_list),
            "custom_text": RuleWrap(None, Alternative([
                Dictation(),
                DictListRef(None, char_dict_list),
                ListRef(None, prefix_list),
                ListRef(None, suffix_list),
                ListRef(None, saved_word_list),
                ])),
            }


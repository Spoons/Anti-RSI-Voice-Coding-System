from dragonfly import (
    Function,
    MappingRule,
    IntegerRef,
    Grammar,
    Dictation
)

from lib.dynamic_aenea import (
    GlobalDynamicContext,
    Key,
    Text,
)

from lib.text import SCText
import lib.format

DYN_MODULE_NAME = "bash"
INCOMPATIBLE_MODULES = []


def directory_up(n):
    repeat = ['..' for i in range(n)]  # @UnusedVariable
    txt = "cd %s\n" % ("/".join(repeat))
    Text(txt).execute()


rules = MappingRule(
    mapping={
        # Commands and keywords:
		"spec <text>": SCText("%(text)s"),
        "apt cache search": Text("apt-cache search "),
        "apt cache search <text>": SCText("apt-cache search %(text)s"),
        "apt cache show": Text("apt-cache show "),
        "apt cache show <text>": SCText("apt-get show %(text)s"),
        "apt get install": Text("apt-get install "),
        "apt get install <text>": SCText("apt-get install %(text)s"),
        "apt get update": Text("apt-get update") + Key("enter"),
        "sudo apt get install": Text("sudo apt-get install "),
        "sudo apt get install <text>": SCText("sudo apt-get install %(text)s"),
        "sudo apt get update": Text("sudo apt-get update") + Key("enter"),
        "background": Text("bg "),
        "cat": Text("cat "),
        "cat <text>": SCText("cat %(text)s"),
        #"(change (directory|dir))": Text("cd "),
        "(change (directory|dir)|seedy) <text>": SCText("cd %(text)s"),
        "[press] control break": Key("ctrl:down, c/10, ctrl:up"),
        "copy": Text("cp "),
        "copy recursive": Text("cp -r "),
        "copy terminal": Key("cs-c/3"),
        "change mode": Text("chmod "),
        "diff": Text("diff "),
        "directory up <n> [times]": Function(directory_up),
        "exit": Text("exit"),
        "foreground": Text("fg "),
        "find process": Text("ps aux | grep -i "),
        "find process <text>": Text("ps aux | grep -i ") + Function(lib.format.snake_case_text),
        "find": Text("find . -iname "),
        "find <text>": SCText("find . -iname %(text)s"),
        "[go to] end of line": Key("c-e"),
        "[go to] start of line": Key("c-a"),
        "grep": Text("grep "),
        "grep invert": Text("grep -v "),
        "grep <text>": SCText("grep %(text)s"),
        "grep invert <text>": SCText("grep -v %(text)s"),
        "grep recursive": Text("grep -rn ") +  Key("dquote/3, dquote/3") + Text(" *") + Key("left/3:3"),  # @IgnorePep8
        "grep recursive <text>": Text("grep -rn ") + Key("dquote/3") + SCText("%(text)s") + Key("dquote/3") + Text(" *") + Key("left/3:3"),  # @IgnorePep8
        "history": Text("history "),
        "ifconfig": Text("ifconfig "),
        "jobs": Text("jobs "),
        "kill": Text("kill "),
        "kill (hard|[dash]9)": Text("kill -9 "),
        "kill line": Key("c-k"),
        "(link|L N)": Text("ln "),
        "list files | ellis": Text("ls -ltra") + Key("enter"),
        "list files <text>": SCText("ls -la %(text)s"),
        "make (directory|dir)": Text("mkdir "),
        "make (directory|dir) <text>": SCText("mkdir %(text)s"),
        "move": Text("mv "),
        "move <text>": SCText("mv %(text)s"),
        "paste terminal": Key("cs-v/3"),
        "pipe": Text(" | "),
        "ping": Text("ping "),
        "(print working directory)": Text("pwd") + Key("enter"),
        "([list] processes [list])": Text("ps -ef"),
        "(remove file)": Text("rm "),
        "(remove file) <text>": SCText("rm %(text)s"),
        "remove (directory|dir|folder|recursive)": Text("rm -rf "),
        "remove (directory|dir|folder|recursive) <text>": SCText("rm -rf %(text)s"),  # @IgnorePep8
        "(sed)": Text("sed "),
        "(secure copy)": Text("scp "),
        "(secure copy) <text>": SCText("scp %(text)s"),
        "(secure shell)": Text("ssh "),
        "(secure shell) <text>": SCText("ssh %(text)s"),
        "soft link": Text("ln -s "),
        "soft link <text>": SCText("ln -s %(text)s"),
        "sudo": Text("sudo "),
        "(switch user)": Text("su "),
        "(switch user) login": Text("su - "),
        "tail": Text("tail "),
        "tail (F|follow)": Text("tail -f "),
        "tail (F|follow) <text>": SCText("tail -f %(text)s"),
        "telnet": Text("telnet "),
        "touch": Text("touch "),
        "touch <text>": SCText("touch %(text)s"),
        "vim": Text("vim "),
        "vim <text>": SCText("vim %(text)s"),
        "word count": Text("wc "),
        "word count lines": Text("wc -l "),
        "W get ": Text("wget "),
        "X args": Text("xargs "),
        "X prop": Text("xprop "),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
    ],
    defaults={
        "n": 1
    }
)

grammar = Grammar("Python grammar", context=GlobalDynamicContext())
grammar.add_rule(rules)
grammar.load()
grammar.disable()


def dynamic_enable():
    global grammar
    if grammar.enabled:
        return False
    else:
        grammar.enable()
        return True


def dynamic_disable():
    global grammar
    if grammar.enabled:
        grammar.disable()
        return True
    else:
        return False


def is_enabled():
    global grammar
    if grammar.enabled:
        return True else:
        return False


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None

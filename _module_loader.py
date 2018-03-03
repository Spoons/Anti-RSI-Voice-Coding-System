import os
import importlib
import natlinkmain

natlink_dir = "C:\\NatLink\\Natlink\\MacroSystem\\"

#name, package
modules = { "multiedit": "multiedit"}

for key, value in modules.iteritems():
    print("Loading %s " % key)
    importlib.import_module(key+'.'+value)


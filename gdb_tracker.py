import gdb
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from tracker.watcher import Watcher
from tracker.emitter import JsonFileEmitter

# Configuration
watched_vars = ["a", "f"]
emitter = JsonFileEmitter("output.json")
watcher = Watcher(watched_vars, emitter)

# This will create a breakpoint when run
class StartHook(gdb.Breakpoint):
    def __init__(self):
        super().__init__("main")

    def stop(self):
        watcher.start()
        return False # Don't pause at main

StartHook()
gdb.execute("set debuginfod enabled off")
gdb.execute("run")

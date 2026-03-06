import gdb
import json
from .extractors import ExtractorRegistry


class Watcher:
    def __init__(self, watched_vars: list[str], emitter, max_steps=100_000):
        print("Initialize Watcher")
        self.watched_vars = watched_vars
        self.emitter = emitter
        self.registry = ExtractorRegistry()
        self.last_snapshots = {}
        self.step_count = 0
        self.max_steps = max_steps
        self.prev_sal = None

    # ------------------------------------------------------------------ #
    #  Lifecycle                                                         #
    # ------------------------------------------------------------------ #

    def start(self):
        # binding the functions to the gdb events
        gdb.events.stop.connect(self._on_stop)
        gdb.events.exited.connect(self._on_exit)
        print("Successfully binding the event functions")
        print("Attempting to Step once")
        gdb.execute("step")

    def stop(self):
        try:
            gdb.events.stop.disconnect(self._on_stop)
            gdb.events.exited.disconnect(self._on_exit)
        except Exception:
            pass

    def _on_exit(self, event):
        if hasattr(self.emitter, "close"):
            self.emitter.close()
        self.stop()

    # ------------------------------------------------------------------ #
    #  Main step loop                                                     #
    # ------------------------------------------------------------------ #

    def _on_stop(self, event):
        # Execute once the program finish a step
        if isinstance(event, gdb.ExitedEvent):
            self.stop()
            return
        if isinstance(event, gdb.SignalEvent):
            self.stop()
            return

        self.step_count += 1
        if self.step_count > self.max_steps:
            self.stop()
            return

        frame = gdb.selected_frame()
        sal = frame.find_sal()

        self.emitter.emit(
            {
                "message": f"{sal.symtab} and {sal.symtab.filename}"
            }
        )
        if not sal.symtab or not sal.symtab.filename.endswith(".c"):
            print("Things are not in the main")
            gdb.execute("finish", to_string=True)
            return

        self.emitter.emit(
            {"message": f"Currently at line {sal.line} and prev is {self.prev_sal.line if self.prev_sal != None else 'None'}"})
        self._check_vars(frame, sal if self.prev_sal ==
                         None else self.prev_sal)
        self.prev_sal = sal
        gdb.execute("step", to_string=True)

    # ------------------------------------------------------------------ #
    #  Variable checking — keyed by (name, scope) pair                   #
    # ------------------------------------------------------------------ #

    def _check_vars(self, frame, sal):
        self.emitter.emit({"message": "checking variables"})
        for var in self.watched_vars:
            try:
                current_value = self.registry.extract(gdb.parse_and_eval(var))
                self.emitter.emit({"message": f"Var {var}: {current_value}"})
            except gdb.error:
                self.emitter.emit({"message": f"Var {var} is out of scope"})
                continue

            if current_value != self.last_snapshots.get(var):
                self.emitter.emit({
                    "variable": var,
                    "new_value": current_value,
                    "file": sal.symtab.filename,
                    "line": sal.line,
                    "function": frame.name()
                })
                self.last_snapshots[var] = current_value

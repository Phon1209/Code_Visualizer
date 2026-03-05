#!/usr/bin/env python3

# gdb -x script.py ./your_program

import gdb
import json
import hashlib
from datetime import datetime
import extract_variable

# TESTING VARIABLES NEED TO CHANGE LATER
G_DEBUG_ENABLE = True


def debug(*args):
    if G_DEBUG_ENABLE:
        print("DEBUG:", args)

class VariableRecorder:
    def __init__(self):
        self.step_count = 0
        self.record_complete = False
        self.variable_state = {}
        self.watching_variables = []
        self.max_step = 1000  # TODO: to be changed
        self.extractor = DataExtractor()

    def program_loop(self):

        gdb.execute("set pagination off")

        self.step_count = 0
        self.record_complete = False

        # Loop until it's out of main
        try:
            gdb.execute("break main", to_string=True)
            gdb.execute("run", to_string=True)
            while not self.record_complete and self.step_count < self.max_step:
                self.step_and_eval()
                self.step_count += 1
        except KeyboardInterrupt:
            print("\nExtraction Interrupted by User\n")
        
        gdb.execute("q")

    def set_watch_variables(self, vars = []):
        if vars == None or vars == []:
            return
        self.watching_variables = vars

    def _is_on_frame(self, func_name="main"):
        ### Find whether a func_name is on the frame stack
        frame = gdb.selected_frame()
        while frame:
            if frame.name() == func_name:
                return frame
            frame = frame.older()
        return None


    def step_and_eval(self):
        # Check whether we're still on our program and not outside to libc part
        try:
            frame = self._is_on_frame("main")
            sal = gdb.selected_frame().find_sal()

            print(f"Found Line {sal.line} on:", frame.name())

        except:
            self.record_complete = True
            print("Frame Check: Out of main")
            return

        # Try Stepping on the codeline
        try:
            gdb.execute("step", to_string=True)
        except gdb.error as e:
            # Check if we've reached the end
            if "not being run" in str(e).lower() or "no stack" in str(e).lower():
                print("✓ Program execution completed")
                self.record_complete = True
                return
            raise


        # Then check for the value
        for var in self.watching_variables:
            print("var", var, "=" ,self.extractor.get_info(var))



recorder = VariableRecorder()
recorder.set_watch_variables(["arr",'arr2d', 'x'])
recorder.program_loop()

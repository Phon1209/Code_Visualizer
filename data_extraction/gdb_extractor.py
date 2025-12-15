#!/usr/bin/env python3

# gdb -x script.py ./your_program

import gdb
import json
import hashlib
from datetime import datetime


class VariableRecorder:
    def __init__(self):
        self.step_count = 0
        self.record_complete = False
        self.variable_state = {}
        self.watching_variables = []
        self.max_step = 4  # TODO: to be changed

    def program_loop(self):
        self.step_count = 0
        self.record_complete = False

        try:
            while not self.record_complete and self.step_count < self.max_step:
                self.step_and_eval()
                self.step_count += 1
        except KeyboardInterrupt:
            print("\nExtraction Interrupted by User\n")

    def step_and_eval(self):
        try:
            gdb.execute("step", to_string=True)
        except gdb.error as e:
            # Check if we've reached the end
            if "not being run" in str(e).lower() or "no stack" in str(e).lower():
                print("✓ Program execution completed")
                self.record_complete = True
                return
            raise

        try:
            frame = gdb.selected_frame()
            func_name = frame.name()

            print(func_name)

        except:
            self.record_complete = True

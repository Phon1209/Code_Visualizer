#!/usr/bin/env python3

# gdb -x script.py ./your_program

import gdb
import json
import hashlib
from datetime import datetime

# TESTING VARIABLES NEED TO CHANGE LATER
G_MAX_ARRAY_SIZE = 40


class VariableRecorder:
    def __init__(self):
        self.step_count = 0
        self.record_complete = False
        self.variable_state = {}
        self.watching_variables = []
        self.max_step = 1000  # TODO: to be changed

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
            print("var", var, "=" ,self.extract_value(var))

    def extract_value(self, var_name):
        try:
            var = gdb.parse_and_eval(var_name)
        except gdb.error:
            # Happen when variable not in scope
            return None
        return self._extract_value(var)
    
    def _extract_value(self, var):
        var_type = var.type
        type_code = var_type.code
        # Find what typedef actually is
        print("TYPE:", str(var_type), "CODE: ", var_type.code)
        print("INT CODE:", gdb.TYPE_CODE_INT, "CHAR CODE: ", gdb.TYPE_CODE_CHAR)
        while type_code == gdb.TYPE_CODE_TYPEDEF:
            # https://sourceware.org/gdb/current/onlinedocs/gdb.html/Types-In-Python.html
            print("TYPE:", str(var_type), "CODE: ", var_type.code)
            var_type = var_type.target()
            type_code = var_type.code

        type_name = str(var_type)
        return_structure = {
            'type': type_name,
            'value': None
        }
        match type_code:
            case gdb.TYPE_CODE_INT:
                print("\nINT\n")
                return_structure['value'] = int(var)
            case gdb.TYPE_CODE_FLT:
                return_structure['value'] = float(var)
            case gdb.TYPE_CODE_BOOL:
                return_structure['value'] = bool(var)
            case gdb.TYPE_CODE_CHAR:
                print("\nCHAR\n")
                val = int(var)
                print(chr(val))
                return_structure['value'] = chr(val) if 32 <= val < 127 else '?' 
            case gdb.TYPE_CODE_ARRAY:
                return self._extract_array(var, var_type)
            case _:
                return_structure['value'] = None
        return return_structure 
    def _extract_array(self, var, var_type):
        """
        """
        # Array type will have range that tell how large the first dimension is 
        try:
            low, high = var_type.range()
            size = high - low + 1

            print("SIZE: ", size)
            elems = []
            elems_type = None
            for i in range(min(size, G_MAX_ARRAY_SIZE)):
                print("EXTRACTING ", i)
                elem = self._extract_value(var[i])
                print(elem)
                elems.append(elem)

            return {
                'type': str(var_type),
                'size': size,
                'elements': elements
            }
        except:
            return {'type': str(var_type), 'error': 'Cannot Extract Value'}


recorder = VariableRecorder()
recorder.set_watch_variables(["arr", 'x'])
recorder.program_loop()

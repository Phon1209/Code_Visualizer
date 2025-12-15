import gdb

gdb.execute("break main", to_string=True)
gdb.execute("run", to_string=True)
gdb.execute("step", to_string=True)

frame = gdb.selected_frame()
while frame:
    print(f"Function: {frame.name()}, PC: {frame.pc()}")
    frame = frame.older()

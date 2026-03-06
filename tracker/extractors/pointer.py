import gdb
from .base import BaseExtractor

class PointerExtractor(BaseExtractor):
    def can_handle(self, val_type):
        return val_type.code == gdb.TYPE_CODE_PTR

    def extract(self, val, context):
        addr = int(val)

        # Null Pointer
        if addr == 0:
            return None

        visited = context["visited"]
        # Pointer is looped
        if addr in visited: 
            return f"<cycle@{addr:#x}>"
        visited.add(addr)

        target_type = val.type.target().strip_typedefs()
        # If it's char*, it's a string
        if target_type.code == gdb.TYPE_CODE_CHAR or \
            (target_type.code == gdb.TYPE_CODE_INT and target_type.sizeof == 1):
            try: 
                return val.string() # gdb will read this until null terminator
            except gdb.error:
                return f"<unreadable string@{addr:#x}>"

        try:
            return context["registry"].extract(val.dereference(), context)
        except gdb.error:
            return f"<unreadable pointer@{addr:#x}>"

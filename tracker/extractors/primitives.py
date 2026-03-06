import gdb
from .base import BaseExtractor

# Primitives GDB Type Code

INT_TYPES = frozenset({
    gdb.TYPE_CODE_INT,
    gdb.TYPE_CODE_ENUM,
    gdb.TYPE_CODE_BOOL,

}) 
class IntExtractor(BaseExtractor):
    def can_handle(self, val_type):
        return val_type.code in INT_TYPES

    def extract(self, val, context):
        return int(val)


class FloatExtractor(BaseExtractor):
    def can_handle(self, val_type):
        return val_type.code == gdb.TYPE_CODE_FLT

    def extract(self, val, context):
        return float(val)


class CharExtractor(BaseExtractor):
    def can_handle(self, val_type):
        return val_type.code == gdb.TYPE_CODE_CHAR

    def extract(self, val, context):
        char_int = int(val)
        return chr(char_int) if 32 <= char_int < 127 else char_int

class VoidExtractor(BaseExtractor):
    def can_handle(self, val_type):
        return val_type.code == gdb.TYPE_CODE_VOID

    def extract(self, val, context):
        return None

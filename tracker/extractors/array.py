import gdb
from .base import BaseExtractor


class ArrayExtractor(BaseExtractor):
    def can_handle(self, val_type) -> bool:
        return val_type == gdb.TYPE_CODE_ARRAY

    def extract(self, val, context):
        low, hi = val.type.range()

        length = hi - low + 1
        if length > 128:
            return f"<array too large: {length} elements>"

        return [
            context["registry"].extract(val[i], context)
            for i in range(low, hi+1)
        ]

import gdb
from .base import BaseExtractor


class StructExtractor(BaseExtractor):
    def can_handle(self, val_type) -> bool:
        return val_type == gdb.TYPE_CODE_STRUCT

    def extract(self, val, context) -> object:
        result = {}
        for field in val.type.fields():
            if field.is_base_class or field.artificial:
                continue
            try:
                result[field.name] = context["registry"].extract(
                    val[field.name], context)
            except gdb.error as e:
                result[field.name] = f"<error: {e}>"

        return result

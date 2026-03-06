import gdb
from .base import BaseExtractor
from .primitives import IntExtractor, FloatExtractor, CharExtractor, VoidExtractor
from .pointer import PointerExtractor

class ExtractorRegistry:
    def __init__(self):
        print("Initialize Registry")
        self._extractors: list[BaseExtractor] = []
        self._register_default_extractors()

    def _register_default_extractors(self):
        """This is the default extractors supported"""

        # Order of register matters - specific extractors first = it will be checked last

        self.register(VoidExtractor())
        self.register(CharExtractor())
        self.register(IntExtractor())
        self.register(FloatExtractor())
        self.register(PointerExtractor())

    def register(self, extractor: BaseExtractor):
        """Adding the Extractor into the register"""
        self._extractors.append(extractor)

    def extract(self, val: gdb.Value, context: dict = None) -> object:
        if context is None:
            context = {"visited": set(), "depth": 0, "registry": self}

        context = {**context, "depth": context["depth"] + 1}

        if context["depth"] > 20:
            return "..."

        val_type = val.type.strip_typedefs()

        for extractor in self._extractors:
            if extractor.can_handle(val_type):
                return extractor.extract(val, context)

        # Fallback to String
        return str(val)

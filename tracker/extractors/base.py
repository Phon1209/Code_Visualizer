import gdb
from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    @abstractmethod
    def can_handle(self, val_type: gdb.Type) -> bool:
        """Return True only if this extractor class can handle the given type"""
        pass

    @abstractmethod
    def extract(self, val: gdb.Value, context: dict) -> object:
        """
        Extract val into a JSON Python object.

        Args:
        context - carries a value that is useful for nested data type i.e. visited addr, depth, registry
        """
        pass

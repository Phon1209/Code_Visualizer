from dataclasses import dataclass

# Frozen dataclass for a class with only data that's immutable


@dataclass(frozen=True)
class WatchedVar:
    name: str
    scope: str  # host a function name where the variable is declared
    # TODO: handle recursive function

    def __str__(self):
        return f"{self.name}@{self.scope}"

import json
import sys
from pathlib import Path


class StdoutEmitter:
    def emit(self, event: dict):
        print(json.dump(event), flush=True)

class JsonFileEmitter:
    """
    Accumulate all events and write them as a JSON array
    """

    def __init__(self, path: str):
        self.path = Path(path)
        self.events: list[dict] = []

    def emit(self, event: dict):
        self.events.append(event)
        self._write()

    def _write(self):
        with open(self.path, "w") as f:
            json.dump(self.events, f, indent=2)

    # just in case
    def close(self):
        self._write()

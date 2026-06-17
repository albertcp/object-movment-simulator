from __future__ import annotations

from pathlib import Path

from logic.messages import PositionMessage

from .base import OutputAdapter


class FileAdapter(OutputAdapter):
    """Appends JSON-serialized position messages to a file."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    def send(self, message: PositionMessage) -> None:
        with self._path.open("a") as f:
            f.write(message.model_dump_json() + "\n")

from __future__ import annotations

import json
import sys

from logic.messages import PositionMessage

from .base import OutputAdapter


class JsonAdapter(OutputAdapter):
    """Serializes PositionMessage to JSON and writes to a file or stdout."""

    def __init__(self, output_path: str | None = None) -> None:
        self._output_path = output_path

    def send(self, message: PositionMessage) -> None:
        data = message.model_dump()
        json_str = json.dumps(data)
        if self._output_path:
            with open(self._output_path, "a") as f:
                f.write(json_str + "\n")
        else:
            print(json_str, file=sys.stdout)

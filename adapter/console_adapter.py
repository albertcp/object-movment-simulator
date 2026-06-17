from __future__ import annotations

from logic.messages import PositionMessage

from .base import OutputAdapter


class ConsoleAdapter(OutputAdapter):
    """Prints formatted position updates to stdout."""

    def send(self, message: PositionMessage) -> None:
        print(
            f"[{message.timestamp:.3f}] "
            f"Object {message.object_id}: "
            f"({message.x:.2f}, {message.y:.2f})"
        )

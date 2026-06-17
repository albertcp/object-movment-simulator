from __future__ import annotations

from logic.messages import PositionMessage

from .base import OutputAdapter


class NetworkAdapter(OutputAdapter):
    """Sends JSON-serialized position messages over a network socket.

    This is a placeholder implementation. Actual transport (WebSocket, UDP)
    should be substituted by a subclass or a strategy pattern.
    """

    def __init__(self, host: str = "localhost", port: int = 0) -> None:
        self._host = host
        self._port = port

    def send(self, message: PositionMessage) -> None:
        raise NotImplementedError(
            f"NetworkAdapter not implemented (host={self._host}, port={self._port})"
        )

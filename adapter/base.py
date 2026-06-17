from __future__ import annotations

from abc import ABC, abstractmethod

from logic.messages import PositionMessage


class OutputAdapter(ABC):
    """Interface for adapters that output object position updates."""

    @abstractmethod
    def send(self, message: PositionMessage) -> None: ...

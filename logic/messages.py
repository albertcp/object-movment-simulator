from __future__ import annotations

from pydantic import BaseModel


class PositionMessage(BaseModel):
    object_id: str
    x: float
    y: float
    timestamp: float

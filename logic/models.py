from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class ObjectState(str, Enum):
    WAITING = "waiting"
    MOVING = "moving"
    ARRIVED = "arrived"


class Position(BaseModel):
    x: float
    y: float


class Path(BaseModel):
    waypoints: list[Position]


class Object(BaseModel):
    id: str
    path: Path
    speed: float
    current_position: Position
    state: ObjectState = ObjectState.WAITING
    current_waypoint_index: int = 0
    progress: float = 0.0


class SimulationState(BaseModel):
    objects: list[Object]
    running: bool = False
    paused: bool = False
    elapsed_time: float = 0.0

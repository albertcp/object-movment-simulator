from __future__ import annotations

from logic.interpolator import PathInterpolator
from logic.models import Object, ObjectState, SimulationState


class SimulationEngine:
    """Manages simulation clock, object updates, and state transitions."""

    def __init__(self, objects: list[Object]) -> None:
        self._objects: list[Object] = [o.model_copy() for o in objects]
        self._running: bool = False
        self._paused: bool = False
        self._elapsed_time: float = 0.0

    @property
    def state(self) -> SimulationState:
        return SimulationState(
            objects=list(self._objects),
            running=self._running,
            paused=self._paused,
            elapsed_time=self._elapsed_time,
        )

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._paused = False
        self._elapsed_time = 0.0
        for obj in self._objects:
            obj.state = ObjectState.MOVING

    def pause(self) -> None:
        if self._running and not self._paused:
            self._paused = True

    def resume(self) -> None:
        if self._running and self._paused:
            self._paused = False

    def stop(self) -> None:
        self._running = False
        self._paused = False

    def reset(self) -> None:
        self._running = False
        self._paused = False
        self._elapsed_time = 0.0
        for obj in self._objects:
            obj.state = ObjectState.WAITING
            obj.current_position = (
                obj.path.waypoints[0] if obj.path.waypoints else obj.current_position
            )
            obj.current_waypoint_index = 0
            obj.progress = 0.0

    def tick(self, dt: float) -> list[Object]:
        """Advance simulation by dt seconds. Returns updated object list."""
        if not self._running or self._paused:
            return list(self._objects)

        self._elapsed_time += dt

        for obj in self._objects:
            if obj.state == ObjectState.ARRIVED:
                continue

            pos, seg_idx, seg_prog = PathInterpolator.compute(
                obj.path, obj.speed, self._elapsed_time
            )
            obj.current_position = pos
            obj.current_waypoint_index = max(0, seg_idx)
            obj.progress = seg_prog

            last_seg = len(obj.path.waypoints) - 2
            if seg_idx >= last_seg and seg_prog >= 1.0:
                obj.state = ObjectState.ARRIVED

        if all(o.state == ObjectState.ARRIVED for o in self._objects):
            self._running = False

        return list(self._objects)

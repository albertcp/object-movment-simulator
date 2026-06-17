from __future__ import annotations

import math

from logic.models import Path, Position


class PathInterpolator:
    """Computes a position along a path given elapsed time and speed."""

    @staticmethod
    def segment_length(start: Position, end: Position) -> float:
        dx = end.x - start.x
        dy = end.y - start.y
        return math.sqrt(dx * dx + dy * dy)

    @staticmethod
    def interpolate(start: Position, end: Position, t: float) -> Position:
        """Linearly interpolate between start and end at parameter t in [0, 1]."""
        return Position(
            x=start.x + (end.x - start.x) * t,
            y=start.y + (end.y - start.y) * t,
        )

    @staticmethod
    def compute(path: Path, speed: float, elapsed_time: float) -> tuple[Position, int, float]:
        """Return (position, segment_index, segment_progress) at elapsed_time.

        segment_progress is in [0, 1] within the current segment.
        segment_index is -1 if before the first waypoint, or the last segment
        index if the object has arrived.
        """
        if not path.waypoints:
            return Position(x=0.0, y=0.0), -1, 0.0

        if len(path.waypoints) == 1:
            return path.waypoints[0], 0, 0.0

        total_distance = speed * elapsed_time
        accumulated = 0.0

        for i in range(len(path.waypoints) - 1):
            seg_len = PathInterpolator.segment_length(path.waypoints[i], path.waypoints[i + 1])
            if total_distance <= accumulated + seg_len or seg_len == 0:
                remaining = total_distance - accumulated
                t = remaining / seg_len if seg_len > 0 else 0.0
                pos = PathInterpolator.interpolate(path.waypoints[i], path.waypoints[i + 1], t)
                return pos, i, t

            accumulated += seg_len

        return path.waypoints[-1], len(path.waypoints) - 2, 1.0

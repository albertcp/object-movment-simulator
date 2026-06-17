from __future__ import annotations

import pytest

from logic.interpolator import PathInterpolator
from logic.models import Path, Position


class TestPathInterpolator:
    def test_empty_path_returns_origin(self) -> None:
        path = Path(waypoints=[])
        pos, seg, prog = PathInterpolator.compute(path, 100.0, 0.0)
        assert pos == Position(x=0.0, y=0.0)
        assert seg == -1
        assert prog == 0.0

    def test_single_waypoint_stays_put(self) -> None:
        path = Path(waypoints=[Position(x=50, y=50)])
        pos, seg, prog = PathInterpolator.compute(path, 100.0, 999.0)
        assert pos == Position(x=50, y=50)
        assert seg == 0
        assert prog == 0.0

    def test_at_start_of_path(self) -> None:
        path = Path(waypoints=[Position(x=0, y=0), Position(x=100, y=0)])
        pos, seg, prog = PathInterpolator.compute(path, 100.0, 0.0)
        assert pos == Position(x=0.0, y=0.0)
        assert seg == 0
        assert prog == 0.0

    def test_mid_segment_horizontal(self) -> None:
        path = Path(waypoints=[Position(x=0, y=0), Position(x=100, y=0)])
        pos, seg, prog = PathInterpolator.compute(path, 100.0, 0.5)
        assert pos.x == pytest.approx(50.0, abs=1e-6)
        assert pos.y == 0.0
        assert seg == 0
        assert prog == pytest.approx(0.5, abs=1e-6)

    def test_mid_segment_vertical(self) -> None:
        path = Path(waypoints=[Position(x=0, y=0), Position(x=0, y=100)])
        pos, seg, prog = PathInterpolator.compute(path, 50.0, 1.0)
        assert pos.x == 0.0
        assert pos.y == pytest.approx(50.0, abs=1e-6)

    def test_diagonal_movement(self) -> None:
        path = Path(waypoints=[Position(x=0, y=0), Position(x=100, y=100)])
        pos, seg, prog = PathInterpolator.compute(path, 141.421, 0.5)
        assert pos.x == pytest.approx(50.0, abs=1.0)
        assert pos.y == pytest.approx(50.0, abs=1.0)

    def test_beyond_path_returns_last_waypoint(self) -> None:
        path = Path(waypoints=[Position(x=0, y=0), Position(x=100, y=0)])
        pos, seg, prog = PathInterpolator.compute(path, 100.0, 10.0)
        assert pos == Position(x=100.0, y=0.0)
        assert seg == 0
        assert prog == 1.0

    def test_multi_segment_path(self) -> None:
        path = Path(
            waypoints=[
                Position(x=0, y=0),
                Position(x=100, y=0),
                Position(x=100, y=100),
            ]
        )
        # After traveling 150 units at speed 100 for 1.5s
        pos, seg, prog = PathInterpolator.compute(path, 100.0, 1.5)
        assert seg == 1
        assert prog == pytest.approx(0.5, abs=1e-6)
        assert pos.x == 100.0
        assert pos.y == 50.0

    def test_zero_length_segment(self) -> None:
        path = Path(
            waypoints=[
                Position(x=10, y=10),
                Position(x=10, y=10),
                Position(x=20, y=10),
            ]
        )
        pos, seg, prog = PathInterpolator.compute(path, 10.0, 0.0)
        assert seg == 0
        assert prog == 0.0

    def test_segment_length_calculation(self) -> None:
        length = PathInterpolator.segment_length(Position(x=0, y=0), Position(x=3, y=4))
        assert length == 5.0

    def test_interpolate_halfway(self) -> None:
        pos = PathInterpolator.interpolate(Position(x=0, y=0), Position(x=10, y=20), 0.5)
        assert pos == Position(x=5.0, y=10.0)

    def test_interpolate_full(self) -> None:
        pos = PathInterpolator.interpolate(Position(x=0, y=0), Position(x=10, y=20), 1.0)
        assert pos == Position(x=10.0, y=20.0)

    def test_interpolate_start(self) -> None:
        pos = PathInterpolator.interpolate(Position(x=5, y=5), Position(x=10, y=10), 0.0)
        assert pos == Position(x=5.0, y=5.0)

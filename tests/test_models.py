from __future__ import annotations

from logic.models import Object, ObjectState, Path, Position, SimulationState


class TestPosition:
    def test_creation(self) -> None:
        p = Position(x=10.0, y=20.0)
        assert p.x == 10.0
        assert p.y == 20.0

    def test_defaults(self) -> None:
        p = Position(x=0.0, y=0.0)
        assert p.x == 0.0


class TestPath:
    def test_creation(self) -> None:
        path = Path(waypoints=[Position(x=0, y=0), Position(x=10, y=10)])
        assert len(path.waypoints) == 2

    def test_empty_path(self) -> None:
        path = Path(waypoints=[])
        assert len(path.waypoints) == 0


class TestObject:
    def test_creation(self) -> None:
        pos = Position(x=0, y=0)
        path = Path(waypoints=[pos, Position(x=10, y=10)])
        o = Object(
            id="test-1",
            path=path,
            speed=50.0,
            current_position=pos,
        )
        assert o.id == "test-1"
        assert o.speed == 50.0
        assert o.state == ObjectState.WAITING
        assert o.current_waypoint_index == 0
        assert o.progress == 0.0

    def test_default_state(self) -> None:
        o = Object(
            id="c1",
            path=Path(waypoints=[Position(x=0, y=0)]),
            speed=10.0,
            current_position=Position(x=0, y=0),
        )
        assert o.state == ObjectState.WAITING


class TestObjectState:
    def test_values(self) -> None:
        assert ObjectState.WAITING.value == "waiting"
        assert ObjectState.MOVING.value == "moving"
        assert ObjectState.ARRIVED.value == "arrived"


class TestSimulationState:
    def test_creation(self) -> None:
        o = Object(
            id="c1",
            path=Path(waypoints=[Position(x=0, y=0)]),
            speed=10.0,
            current_position=Position(x=0, y=0),
        )
        s = SimulationState(objects=[o])
        assert len(s.objects) == 1
        assert s.running is False
        assert s.paused is False
        assert s.elapsed_time == 0.0

    def test_running_flag(self) -> None:
        s = SimulationState(objects=[], running=True)
        assert s.running is True

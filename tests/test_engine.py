from __future__ import annotations

from logic.engine import SimulationEngine
from logic.models import Object, ObjectState, Path, Position


def _make_object(cid: str = "c1", waypoints: list[Position] | None = None) -> Object:
    wps = waypoints or [Position(x=0, y=0), Position(x=100, y=0)]
    return Object(
        id=cid,
        path=Path(waypoints=wps),
        speed=100.0,
        current_position=wps[0],
        state=ObjectState.WAITING,
    )


class TestSimulationEngine:
    def test_initial_state_is_stopped(self) -> None:
        engine = SimulationEngine([_make_object()])
        state = engine.state
        assert state.running is False
        assert state.paused is False
        assert state.elapsed_time == 0.0

    def test_empty_objects_list(self) -> None:
        engine = SimulationEngine([])
        state = engine.state
        assert state.objects == []

    def test_start_sets_moving_state(self) -> None:
        engine = SimulationEngine([_make_object()])
        engine.start()
        state = engine.state
        assert state.running is True
        assert state.paused is False
        for o in state.objects:
            assert o.state == ObjectState.MOVING

    def test_start_idempotent(self) -> None:
        engine = SimulationEngine([_make_object()])
        engine.start()
        engine.start()
        state = engine.state
        assert state.running is True

    def test_pause_and_resume(self) -> None:
        engine = SimulationEngine([_make_object()])
        engine.start()
        engine.pause()
        assert engine.state.paused is True
        engine.resume()
        assert engine.state.paused is False

    def test_pause_when_not_running_does_nothing(self) -> None:
        engine = SimulationEngine([_make_object()])
        engine.pause()
        assert engine.state.paused is False

    def test_resume_when_not_paused_does_nothing(self) -> None:
        engine = SimulationEngine([_make_object()])
        engine.start()
        engine.resume()
        assert engine.state.paused is False

    def test_stop(self) -> None:
        engine = SimulationEngine([_make_object()])
        engine.start()
        engine.stop()
        state = engine.state
        assert state.running is False
        assert state.paused is False

    def test_reset(self) -> None:
        engine = SimulationEngine([_make_object()])
        engine.start()
        engine.tick(1.0)
        engine.reset()
        state = engine.state
        assert state.running is False
        assert state.elapsed_time == 0.0
        for o in state.objects:
            assert o.state == ObjectState.WAITING
            assert o.current_position.x == 0.0

    def test_tick_moves_object(self) -> None:
        engine = SimulationEngine([_make_object()])
        engine.start()
        objects = engine.tick(0.5)
        assert objects[0].current_position.x == 50.0

    def test_tick_no_movement_when_paused(self) -> None:
        engine = SimulationEngine([_make_object()])
        engine.start()
        engine.pause()
        objects = engine.tick(1.0)
        assert objects[0].current_position.x == 0.0

    def test_tick_no_movement_when_stopped(self) -> None:
        engine = SimulationEngine([_make_object()])
        objects = engine.tick(1.0)
        assert objects[0].current_position.x == 0.0

    def test_arrival_detection(self) -> None:
        engine = SimulationEngine([_make_object()])
        engine.start()
        engine.tick(10.0)
        assert engine.state.objects[0].state == ObjectState.ARRIVED

    def test_all_arrived_stops_simulation(self) -> None:
        engine = SimulationEngine([_make_object()])
        engine.start()
        engine.tick(10.0)
        assert engine.state.running is False

    def test_mixed_arrival_status(self) -> None:
        o1 = _make_object("o1", [Position(x=0, y=0), Position(x=100, y=0)])
        o2 = _make_object("o2", [Position(x=0, y=0), Position(x=200, y=0)])
        engine = SimulationEngine([o1, o2])
        engine.start()
        engine.tick(1.5)
        # o1 arrived (100 units @ 100/s = 1s), o2 still moving (200 units @ 100/s = 2s)
        assert engine.state.objects[0].state == ObjectState.ARRIVED
        assert engine.state.objects[1].state == ObjectState.MOVING
        assert engine.state.running is True

    def test_tick_returns_objects_copy(self) -> None:
        engine = SimulationEngine([_make_object()])
        engine.start()
        result = engine.tick(0.5)
        result[0].current_position = Position(x=999, y=999)
        # Should not affect engine's internal state
        objects2 = engine.tick(0.0)
        assert objects2[0].current_position.x != 999

    def test_tick_with_no_objects(self) -> None:
        engine = SimulationEngine([])
        engine.start()
        objects = engine.tick(1.0)
        assert objects == []
        assert engine.state.running is False

    def test_start_after_arrival_and_reset(self) -> None:
        engine = SimulationEngine([_make_object()])
        engine.start()
        engine.tick(10.0)
        assert engine.state.running is False
        engine.reset()
        engine.start()
        assert engine.state.running is True
        assert engine.state.objects[0].state == ObjectState.MOVING

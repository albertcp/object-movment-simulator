from __future__ import annotations

import json
from pathlib import Path as FilePath

import pytest

from adapter.file_adapter import FileAdapter
from logic.engine import SimulationEngine
from logic.messages import PositionMessage
from logic.models import Object, ObjectState, Path, Position


def _object(cid: str, waypoints: list[Position]) -> Object:
    return Object(
        id=cid,
        path=Path(waypoints=waypoints),
        speed=100.0,
        current_position=waypoints[0],
        state=ObjectState.WAITING,
    )


class TestFullSimulationCycle:
    def test_single_object_full_path(self, tmp_path: FilePath) -> None:
        obj = _object("c1", [Position(x=0, y=0), Position(x=100, y=0)])
        engine = SimulationEngine([obj])
        engine.start()

        positions_at: dict[float, tuple[float, float]] = {}
        for _ in range(60):
            dt = 1.0 / 60.0
            objects = engine.tick(dt)
            elapsed = engine.state.elapsed_time
            for obj in objects:
                pos = obj.current_position
                positions_at[round(elapsed, 3)] = (pos.x, pos.y)
            if not engine.state.running:
                break

        assert not engine.state.running
        assert engine.state.objects[0].state == ObjectState.ARRIVED

        # Verify final position
        final = engine.state.objects[0].current_position
        assert final.x == pytest.approx(100.0, abs=1.0)
        assert final.y == 0.0

    def test_multiple_objects_independent_paths(self) -> None:
        o1 = _object("fast", [Position(x=0, y=0), Position(x=100, y=0)])
        o2 = _object("slow", [Position(x=0, y=0), Position(x=50, y=0)])
        o2.speed = 50.0
        engine = SimulationEngine([o1, o2])
        engine.start()
        engine.tick(1.0)
        assert engine.state.objects[0].current_position.x == pytest.approx(100.0, abs=1.0)
        assert engine.state.objects[1].current_position.x == pytest.approx(50.0, abs=1.0)
        assert engine.state.objects[0].state == ObjectState.ARRIVED
        assert engine.state.objects[1].state == ObjectState.ARRIVED

    def test_start_pause_resume_flow(self) -> None:
        obj = _object("c1", [Position(x=0, y=0), Position(x=100, y=0)])
        engine = SimulationEngine([obj])
        engine.start()
        engine.tick(0.5)
        assert engine.state.objects[0].current_position.x == 50.0
        engine.pause()
        engine.tick(100.0)
        assert engine.state.objects[0].current_position.x == 50.0
        engine.resume()
        engine.tick(0.5)
        assert engine.state.objects[0].current_position.x == 100.0

    def test_file_output_end_to_end(self, tmp_path: FilePath) -> None:
        out = tmp_path / "sim.jsonl"
        adapter = FileAdapter(path=out)
        obj = _object("c1", [Position(x=10, y=10), Position(x=20, y=10)])
        engine = SimulationEngine([obj])
        engine.start()

        while engine.state.running:
            objects = engine.tick(0.1)
            for obj in objects:
                adapter.send(
                    PositionMessage(
                        object_id=obj.id,
                        x=obj.current_position.x,
                        y=obj.current_position.y,
                        timestamp=engine.state.elapsed_time,
                    )
                )

        lines = out.read_text().strip().split("\n")
        assert len(lines) > 0
        last = json.loads(lines[-1])
        assert last["object_id"] == "c1"

    def test_reset_and_restart(self) -> None:
        obj = _object("c1", [Position(x=0, y=0), Position(x=100, y=0)])
        engine = SimulationEngine([obj])
        engine.start()
        engine.tick(10.0)
        assert engine.state.objects[0].state is ObjectState.ARRIVED
        engine.reset()
        assert engine.state.objects[0].state is ObjectState.WAITING  # type: ignore[comparison-overlap]
        assert engine.state.objects[0].current_position.x == 0.0
        engine.start()
        engine.tick(0.5)
        assert engine.state.objects[0].current_position.x == 50.0

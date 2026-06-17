from __future__ import annotations

from unittest.mock import MagicMock, patch

import pygame
import pytest

from controller.app import App
from logic.engine import SimulationEngine
from logic.models import Object, ObjectState, Path, Position


@pytest.fixture
def engine() -> SimulationEngine:
    o = Object(
        id="c1",
        path=Path(waypoints=[Position(x=0, y=0), Position(x=100, y=0)]),
        speed=100.0,
        current_position=Position(x=0, y=0),
        state=ObjectState.WAITING,
    )
    return SimulationEngine([o])


@pytest.fixture
def app(engine: SimulationEngine) -> App:
    with (
        patch("pygame.display.set_mode", return_value=MagicMock(spec=pygame.Surface)),
        patch("pygame.display.set_caption"),
        patch("pygame.font.SysFont", return_value=MagicMock()),
    ):
        return App(engine)


class TestApp:
    def test_initialization(self, app: App) -> None:
        assert app._ui is not None
        assert app._selected_index is None
        assert app._sim_complete is False

    def test_handle_space_starts_simulation(self, app: App) -> None:
        assert app._engine.state.running is False
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        app._handle_event(event)
        assert app._engine.state.running is True

    def test_handle_space_pauses(self, app: App) -> None:
        app._engine.start()
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        app._handle_event(event)
        assert app._engine.state.paused is True

    def test_handle_space_resumes(self, app: App) -> None:
        app._engine.start()
        app._engine.pause()
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        app._handle_event(event)
        assert app._engine.state.paused is False

    def test_handle_r_resets(self, app: App) -> None:
        app._engine.start()
        app._engine.tick(1.0)
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_r})
        app._handle_event(event)
        assert app._engine.state.running is False
        assert app._engine.state.elapsed_time == 0.0

    def test_handle_delete_removes_object(self, app: App) -> None:
        app._selected_index = 0
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DELETE})
        app._handle_event(event)
        assert len(app._engine.state.objects) == 0
        assert app._selected_index is None

    def test_handle_delete_blocked_during_simulation(self, app: App) -> None:
        app._engine.start()
        app._selected_index = 0
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DELETE})
        app._handle_event(event)
        assert len(app._engine.state.objects) == 1

    def test_hit_test_object_hits(self, app: App) -> None:
        o = app._engine.state.objects[0]
        # Object is at (0, 0), click at (5, 5) is within hit radius
        pos = (int(o.current_position.x + 5), int(o.current_position.y + 5))
        index = app._hit_test_object(pos)
        assert index == 0

    def test_hit_test_object_misses(self, app: App) -> None:
        index = app._hit_test_object((500, 500))
        assert index is None

    def test_hit_test_object_no_objects(self) -> None:
        empty_engine = SimulationEngine([])
        with (
            patch("pygame.display.set_mode", return_value=MagicMock(spec=pygame.Surface)),
            patch("pygame.display.set_caption"),
            patch("pygame.font.SysFont", return_value=MagicMock()),
        ):
            empty_app = App(empty_engine)
        index = empty_app._hit_test_object((50, 50))
        assert index is None

    def test_mouse_click_selects_object(self, app: App) -> None:
        app._ui._placing = False
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (200, 200)})
        app._handle_event(event)
        assert app._selected_index is None  # no object at (200, 200)

    def test_mouse_click_on_panel_ignored(self, app: App) -> None:
        app._ui._placing = False
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (10, 10)})
        app._handle_event(event)
        assert app._selected_index is None

    def test_mouse_click_adds_waypoint(self, app: App) -> None:
        app._ui._placing = True
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (200, 300)})
        app._handle_event(event)
        assert len(app._ui.pending_waypoints) == 1

    def test_update_sends_messages(self, app: App) -> None:
        mock_adapter = MagicMock()
        app._adapters = [mock_adapter]
        app._engine.start()
        app._update(0.5)
        assert mock_adapter.send.call_count == 1

    def test_update_no_messages_when_stopped(self, app: App) -> None:
        mock_adapter = MagicMock()
        app._adapters = [mock_adapter]
        app._update(0.5)
        assert mock_adapter.send.call_count == 0

    def test_update_updates_objects(self, app: App) -> None:
        app._engine.start()
        app._update(0.5)
        assert app._engine.state.objects[0].current_position.x == 50.0

    @patch("pygame.font.SysFont", return_value=MagicMock())
    def test_draw_complete_overlay(self, mock_font: MagicMock, app: App) -> None:
        app._sim_complete = True
        app._draw_complete_overlay()

    @patch("pygame.draw.circle")
    @patch("pygame.draw.lines")
    @patch("pygame.font.SysFont")
    def test_draw_object_path(
        self, mock_font: MagicMock, mock_lines: MagicMock, mock_circle: MagicMock, app: App
    ) -> None:
        obj = Object(
            id="multi",
            path=Path(waypoints=[Position(x=0, y=0), Position(x=100, y=0), Position(x=100, y=100)]),
            speed=100.0,
            current_position=Position(x=100, y=0),
        )
        app._draw_object_path(obj)

    @patch("pygame.draw.circle")
    @patch("pygame.font.SysFont")
    def test_draw_object(self, mock_font: MagicMock, mock_circle: MagicMock, app: App) -> None:
        obj = Object(
            id="draw-test",
            path=Path(waypoints=[Position(x=50, y=50)]),
            speed=100.0,
            current_position=Position(x=50, y=50),
        )
        app._draw_object(obj, 0)

    @patch("pygame.draw.circle")
    @patch("pygame.font.SysFont")
    def test_draw_object_arrived(
        self, mock_font: MagicMock, mock_circle: MagicMock, app: App
    ) -> None:
        obj = Object(
            id="arrived-test",
            path=Path(waypoints=[Position(x=100, y=100)]),
            speed=100.0,
            current_position=Position(x=100, y=100),
            state=ObjectState.ARRIVED,
        )
        app._draw_object(obj, 0)

    @patch("pygame.draw.circle")
    @patch("pygame.font.SysFont")
    def test_draw_object_selected(
        self, mock_font: MagicMock, mock_circle: MagicMock, app: App
    ) -> None:
        app._selected_index = 0
        obj = app._engine.state.objects[0]
        app._draw_object(obj, 0)

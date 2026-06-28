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

    def test_add_object_button_creates_engine_object(self, app: App) -> None:
        # Enter placing mode and add waypoints
        app._ui._placing = True
        app._ui.add_waypoint(Position(x=10, y=10))
        app._ui.add_waypoint(Position(x=100, y=100))
        app._ui.add_waypoint(Position(x=200, y=200))
        assert len(app._engine.state.objects) == 1  # original fixture object

        # Click the Add object button (panel x=15, y=20)
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (15, 20)})
        app._handle_event(event)
        assert len(app._engine.state.objects) == 2
        added = app._engine.state.objects[1]
        assert added.id == "Object-1"
        assert len(added.path.waypoints) == 3

    def test_multiple_add_object_clicks_create_multiple_objects(self, app: App) -> None:
        assert len(app._engine.state.objects) == 1  # original fixture object

        # Add first object
        app._ui._placing = True
        app._ui.add_waypoint(Position(x=0, y=0))
        app._ui.add_waypoint(Position(x=50, y=50))
        event1 = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (15, 20)})
        app._handle_event(event1)
        assert len(app._engine.state.objects) == 2

        # Add second object
        app._ui._placing = False
        event_enter = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (15, 20)})
        app._handle_event(event_enter)  # enters placing mode
        app._ui.add_waypoint(Position(x=100, y=100))
        app._ui.add_waypoint(Position(x=200, y=200))
        app._ui.add_waypoint(Position(x=300, y=300))
        event2 = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (15, 20)})
        app._handle_event(event2)
        assert len(app._engine.state.objects) == 3

        # Verify both new objects with correct IDs
        obj1 = app._engine.state.objects[1]
        obj2 = app._engine.state.objects[2]
        assert obj1.id == "Object-1"
        assert obj2.id == "Object-2"
        assert len(obj1.path.waypoints) == 2
        assert len(obj2.path.waypoints) == 3

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

    def test_draw_complete_overlay(self, app: App) -> None:
        app._sim_complete = True
        app._draw_complete_overlay()

    @patch("pygame.draw.circle")
    @patch("pygame.draw.lines")
    def test_draw_object_path(
        self, mock_lines: MagicMock, mock_circle: MagicMock, app: App
    ) -> None:
        obj = Object(
            id="multi",
            path=Path(waypoints=[Position(x=0, y=0), Position(x=100, y=0), Position(x=100, y=100)]),
            speed=100.0,
            current_position=Position(x=100, y=0),
        )
        app._draw_object_path(obj)

    @patch("pygame.draw.circle")
    def test_draw_object(self, mock_circle: MagicMock, app: App) -> None:
        obj = Object(
            id="draw-test",
            path=Path(waypoints=[Position(x=50, y=50)]),
            speed=100.0,
            current_position=Position(x=50, y=50),
        )
        app._draw_object(obj, 0)

    @patch("pygame.draw.circle")
    def test_draw_object_arrived(self, mock_circle: MagicMock, app: App) -> None:
        obj = Object(
            id="arrived-test",
            path=Path(waypoints=[Position(x=100, y=100)]),
            speed=100.0,
            current_position=Position(x=100, y=100),
            state=ObjectState.ARRIVED,
        )
        app._draw_object(obj, 0)

    @patch("pygame.draw.circle")
    def test_draw_object_selected(self, mock_circle: MagicMock, app: App) -> None:
        app._selected_index = 0
        obj = app._engine.state.objects[0]
        app._draw_object(obj, 0)

    # ── Speed editing integration tests ──────────────────────────────────

    def test_edit_speed_click_enters_editing_mode(self, app: App) -> None:
        """Clicking Edit Speed through App enters editing mode."""
        app._selected_index = 0
        app._ui.set_selected_object(app._engine.state.objects[0])
        app._ui._editing_speed = False
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (15, 70)})
        app._handle_event(event)
        assert app._ui._editing_speed is True
        assert float(app._ui._speed_input_text) > 0

    def test_edit_speed_click_without_selection_does_nothing(self, app: App) -> None:
        """Clicking Edit Speed without an object selected does nothing."""
        app._selected_index = None
        app._ui._editing_speed = False
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (15, 70)})
        app._handle_event(event)
        assert app._ui._editing_speed is False

    def test_edit_speed_keyboard_digit_updates_input(self, app: App) -> None:
        """Typing a digit during speed editing updates the input text."""
        app._selected_index = 0
        app._ui.set_selected_object(app._engine.state.objects[0])
        app._ui._editing_speed = True
        app._ui._speed_input_text = ""
        event = pygame.event.Event(pygame.KEYDOWN, {"key": ord("5"), "unicode": "5"})
        app._handle_event(event)
        assert app._ui._speed_input_text == "5"

    def test_edit_speed_keyboard_decimal_updates_input(self, app: App) -> None:
        """Typing a decimal point during speed editing updates the input."""
        app._selected_index = 0
        app._ui.set_selected_object(app._engine.state.objects[0])
        app._ui._editing_speed = True
        app._ui._speed_input_text = "10"
        event = pygame.event.Event(pygame.KEYDOWN, {"key": ord("."), "unicode": "."})
        app._handle_event(event)
        assert app._ui._speed_input_text == "10."

    def test_edit_speed_keyboard_non_numeric_ignored(self, app: App) -> None:
        """Non-numeric key presses are ignored during speed editing."""
        app._selected_index = 0
        app._ui.set_selected_object(app._engine.state.objects[0])
        app._ui._editing_speed = True
        app._ui._speed_input_text = "50"
        event = pygame.event.Event(pygame.KEYDOWN, {"key": ord("a"), "unicode": "a"})
        app._handle_event(event)
        assert app._ui._speed_input_text == "50"

    def test_edit_speed_keyboard_backspace_removes_char(self, app: App) -> None:
        """Backspace removes the last input character during speed editing."""
        app._selected_index = 0
        app._ui.set_selected_object(app._engine.state.objects[0])
        app._ui._editing_speed = True
        app._ui._speed_input_text = "100"
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_BACKSPACE, "unicode": "\x08"})
        app._handle_event(event)
        assert app._ui._speed_input_text == "10"

    def test_edit_speed_enter_updates_engine_speed(self, app: App) -> None:
        """Pressing Enter confirms speed and updates engine object."""
        app._selected_index = 0
        app._ui.set_selected_object(app._engine.state.objects[0])
        app._ui._editing_speed = True
        app._ui._speed_input_text = "50.0"
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "unicode": "\r"})
        app._handle_event(event)
        assert app._engine.state.objects[0].speed == 50.0
        assert app._ui._editing_speed is False

    def test_edit_speed_enter_invalid_value_keeps_editing(self, app: App) -> None:
        """Pressing Enter with invalid speed keeps editing mode active."""
        app._selected_index = 0
        app._ui.set_selected_object(app._engine.state.objects[0])
        app._ui._editing_speed = True
        app._ui._speed_input_text = "-5"
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "unicode": "\r"})
        app._handle_event(event)
        # Speed should remain unchanged
        assert app._engine.state.objects[0].speed == 100.0

    def test_edit_speed_escape_cancels(self, app: App) -> None:
        """Pressing Escape cancels speed editing without changing speed."""
        app._selected_index = 0
        original_speed = app._engine.state.objects[0].speed
        app._ui.set_selected_object(app._engine.state.objects[0])
        app._ui._editing_speed = True
        app._ui._speed_input_text = "999.0"
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE, "unicode": "\x1b"})
        app._handle_event(event)
        assert app._engine.state.objects[0].speed == original_speed
        assert app._ui._editing_speed is False

    def test_edit_speed_updated_speed_used_in_tick(self, app: App) -> None:
        """After editing speed, the object moves at the new speed."""
        app._selected_index = 0
        app._ui.set_selected_object(app._engine.state.objects[0])
        # Create a longer path so the object doesn't arrive before 1s
        obj = Object(
            id="speed-test",
            path=Path(waypoints=[Position(x=0, y=0), Position(x=500, y=0)]),
            speed=200.0,
            current_position=Position(x=0, y=0),
            state=ObjectState.WAITING,
        )
        app._engine = SimulationEngine([obj])
        app._engine.start()
        app._update(1.0)
        # At speed 200, after 1s it should be at x=200
        assert app._engine.state.objects[0].current_position.x == 200.0

    # ── Objects list integration tests ───────────────────────────────────

    def test_objects_list_passed_to_ui(self, app: App) -> None:
        """App passes engine objects to UIPanel via set_objects."""
        objects_before = list(app._engine.state.objects)
        # Simulate what _draw does
        app._ui.set_objects(objects_before)
        assert len(app._ui._objects) == len(objects_before)
        assert app._ui._objects[0].id == objects_before[0].id

    def test_objects_list_updates_with_engine_changes(self, app: App) -> None:
        """After adding an object, the UI objects list reflects the change."""
        initial_count = len(app._engine.state.objects)
        new_obj = Object(
            id="new-obj",
            path=Path(waypoints=[Position(x=0, y=0), Position(x=100, y=100)]),
            speed=50.0,
            current_position=Position(x=0, y=0),
        )
        new_engine = SimulationEngine(list(app._engine.state.objects) + [new_obj])
        app._engine = new_engine
        app._ui.set_objects(list(app._engine.state.objects))
        assert len(app._ui._objects) == initial_count + 1
        assert app._ui._objects[1].id == "new-obj"

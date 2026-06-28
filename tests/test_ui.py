from __future__ import annotations

from controller.ui import Button, UIPanel
from logic.models import Object, ObjectState, Path, Position


class TestButton:
    def test_clicked_within_rect(self) -> None:
        btn = Button(x=10, y=10, text="Test")
        assert btn.clicked((20, 20)) is True

    def test_clicked_outside_rect(self) -> None:
        btn = Button(x=10, y=10, text="Test")
        assert btn.clicked((500, 500)) is False

    def test_update_sets_hovered(self) -> None:
        btn = Button(x=10, y=10, text="Test")
        btn.update((20, 20))
        assert btn._hovered is True

    def test_update_clears_hovered(self) -> None:
        btn = Button(x=10, y=10, text="Test")
        btn.update((500, 500))
        assert btn._hovered is False


class TestUIPanel:
    def test_initial_state(self) -> None:
        panel = UIPanel()
        assert panel.placing is False
        assert panel.pending_waypoints == []

    def test_placing_toggle_on_add_click(self) -> None:
        panel = UIPanel()
        result = panel.handle_click((15, 20))
        assert result is None
        assert panel.placing is True

    def test_add_waypoint(self) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))  # enter placing mode
        panel.add_waypoint(Position(x=100, y=200))
        assert len(panel.pending_waypoints) == 1
        assert panel.pending_waypoints[0] == Position(x=100, y=200)

    def test_remove_last_waypoint(self) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))
        panel.add_waypoint(Position(x=100, y=200))
        panel.add_waypoint(Position(x=300, y=400))
        panel.remove_last_waypoint()
        assert len(panel.pending_waypoints) == 1

    def test_clear_path(self) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))
        panel.add_waypoint(Position(x=100, y=200))
        panel.add_waypoint(Position(x=300, y=400))
        panel.clear_path()
        assert panel.pending_waypoints == []

    def test_finish_drawing_creates_object(self) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))
        panel.add_waypoint(Position(x=10, y=10))
        panel.add_waypoint(Position(x=20, y=20))
        result = panel.finish_drawing()
        assert result is not None
        action, obj = result
        assert action == "add_object"
        assert obj.id == "Object-1"
        assert obj.speed == 100.0
        assert obj.state == ObjectState.WAITING

    def test_finish_drawing_empty_returns_none(self) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))
        result = panel.finish_drawing()
        assert result is None
        assert panel.placing is False

    def test_play_button_click(self) -> None:
        panel = UIPanel()
        result = panel.handle_click((15, 70))
        assert result == "play"

    def test_reset_button_click(self) -> None:
        panel = UIPanel()
        result = panel.handle_click((15, 120))
        assert result == "reset"

    def test_set_selected_object(self) -> None:
        panel = UIPanel()
        obj = Object(
            id="c1",
            path=Path(waypoints=[Position(x=0, y=0)]),
            speed=50.0,
            current_position=Position(x=10, y=10),
        )
        panel.set_selected_object(obj)
        assert panel._selected_object is not None

    def test_disable_during_simulation(self) -> None:
        panel = UIPanel()
        panel.sync_state(running=True, paused=False)
        result = panel.handle_click((15, 20))  # add object
        assert result is None
        assert panel.placing is False

    def test_add_button_label(self) -> None:
        panel = UIPanel()
        assert panel._add_btn.text == "Add object"

    def test_add_click_creates_object_when_placing_with_waypoints(self) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))  # enter placing mode
        panel.add_waypoint(Position(x=10, y=10))
        panel.add_waypoint(Position(x=20, y=20))
        panel.add_waypoint(Position(x=30, y=30))
        result = panel.handle_click((15, 20))  # press Add button again
        assert isinstance(result, tuple)
        action, obj = result
        assert action == "add_object"
        assert obj.id == "Object-1"
        assert len(obj.path.waypoints) == 3
        assert obj.state == ObjectState.WAITING
        assert panel.placing is False  # exited placing mode

    def test_add_click_toggles_placing_without_waypoints(self) -> None:
        panel = UIPanel()
        # First click: enter placing mode
        panel.handle_click((15, 20))
        assert panel.placing is True
        # Second click: exit placing mode (no waypoints, no object)
        result = panel.handle_click((15, 20))
        assert result is None
        assert panel.placing is False

    def test_multiple_objects_creation_sequence(self) -> None:
        panel = UIPanel()
        # --- Create first object ---
        panel.handle_click((15, 20))  # enter placing
        panel.add_waypoint(Position(x=0, y=0))
        panel.add_waypoint(Position(x=50, y=50))
        result1 = panel.handle_click((15, 20))  # finish first object
        assert isinstance(result1, tuple)
        action1, obj1 = result1
        assert action1 == "add_object"
        assert obj1.id == "Object-1"
        assert panel.placing is False

        # --- Create second object ---
        panel.handle_click((15, 20))  # enter placing again
        panel.add_waypoint(Position(x=100, y=100))
        panel.add_waypoint(Position(x=200, y=200))
        panel.add_waypoint(Position(x=300, y=300))
        result2 = panel.handle_click((15, 20))  # finish second object
        assert isinstance(result2, tuple)
        action2, obj2 = result2
        assert action2 == "add_object"
        assert obj2.id == "Object-2"
        assert len(obj2.path.waypoints) == 3
        assert panel.placing is False

        # Objects are independent
        assert obj1.id != obj2.id
        assert len(obj1.path.waypoints) == 2
        assert len(obj2.path.waypoints) == 3

    def test_add_button_locked_in_placing_mode(self) -> None:
        """Button is 'locked' while placing: pressing it finalizes the object."""
        panel = UIPanel()
        panel.handle_click((15, 20))  # enter placing
        panel.add_waypoint(Position(x=10, y=10))
        panel.add_waypoint(Position(x=20, y=20))

        # While placing, button click creates object (does not just toggle)
        result = panel.handle_click((15, 20))
        assert isinstance(result, tuple)
        _, obj = result
        assert obj.id == "Object-1"

        # After creation, placing is exited - button is "unlocked"
        assert panel.placing is False

        # Now click again: enters placing mode fresh
        panel.handle_click((15, 20))
        assert panel.placing is True
